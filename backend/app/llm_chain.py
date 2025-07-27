# backend/app/llm_chain.py

import os
import re
import logging
from sqlalchemy import create_engine, text, inspect
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env variables
load_dotenv()

# === ✅ Database Configuration ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../sql_app.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# === ✅ Data Dictionary with Detailed Schema ===
DATA_DICTIONARY = """
You are an intelligent assistant for an e-commerce platform. Answer user queries using the following EXACT table schemas:

1. distribution_centers: [id, name, latitude, longitude]
2. inventory_items: [id, product_id, created_at, sold_at, cost, product_category, product_name, product_brand, product_retail_price, product_department, product_sku, product_distribution_center_id]
3. order_items: [id, order_id, user_id, product_id, inventory_item_id, status, created_at, shipped_at, delivered_at, returned_at]
4. orders: [order_id, user_id, status, gender, created_at, returned_at, shipped_at, delivered_at, num_of_item]
5. products: [id, cost, category, name, brand, retail_price, department, sku, distribution_center_id]
6. users: [id, first_name, last_name, email, age, gender, state, street_address, postal_code, city, country, latitude, longitude, traffic_source, created_at]

CRITICAL NOTES:
- The 'products' table has 'name' NOT 'product_name'
- Use 'products.name' for product names
- 'inventory_items.product_name' is historical name at time of inventory creation
- For current product names, ALWAYS use 'products.name'

Important Instructions:
- Use JOINs where necessary
- Be precise and concise in responses
- Never modify the data
- Answer in 1-2 sentences maximum
- Format numerical results clearly
"""

# === ✅ LLM Configuration ===
llm = ChatGroq(
    temperature=0.1,
    model_name="llama3-70b-8192",
    api_key=os.environ["GROQ_API_KEY"]
)

# === ✅ Prompt Templates ===
SQL_PROMPT = PromptTemplate(
    template="""
{data_dictionary}

Database Schema:
{table_info}

Instructions:
1. Generate ONLY the SQL query
2. Use SQLite syntax
3. Be precise with table/column names
4. If clarification needed, return "CLARIFY: [your question]"

Question: {question}
SQL Query:
""".strip(),
    input_variables=["question", "table_info"]
).partial(data_dictionary=DATA_DICTIONARY)

RESPONSE_PROMPT = PromptTemplate(
    template="""
{data_dictionary}

Instructions:
1. Answer concisely (1-2 sentences)
2. Use simple, direct language
3. Format numbers clearly
4. If no results, say "No matching information found"

User Question: {question}
SQL Used: {sql}
Query Results: {result}

Concise Response:
""".strip(),
    input_variables=["question", "sql", "result"]
).partial(data_dictionary=DATA_DICTIONARY)

# === ✅ Runnable Sequences ===
# SQL generation sequence
sql_sequence = RunnableSequence(
    RunnablePassthrough.assign(table_info=lambda x: get_table_info()),
    SQL_PROMPT,
    llm,
    StrOutputParser()
)

# Response generation sequence
response_sequence = RunnableSequence(
    RESPONSE_PROMPT,
    llm,
    StrOutputParser()
)

# === ✅ Helper Functions ===
def get_table_info():
    """Get detailed schema information"""
    inspector = inspect(engine)
    table_info = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_info = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
        table_info.append(f"Table: {table_name}\nColumns: {column_info}")
    
    return "\n\n".join(table_info)

def clean_sql(sql: str) -> str:
    """Extract clean SQL query"""
    # Remove markdown code blocks
    if '```sql' in sql:
        sql = re.sub(r'```sql|```', '', sql)
    
    # Extract first SQL statement
    sql = sql.split(';')[0].strip()
    
    # Remove non-SQL text
    return re.sub(r'^[^SELECT]*(SELECT)', 'SELECT', sql, flags=re.IGNORECASE)

def validate_sql(sql: str) -> bool:
    """Validate SQL against known issues"""
    # Check for invalid product_name reference
    if "products.product_name" in sql.lower():
        logger.error("Invalid column reference: products.product_name")
        return False
        
    return True

# === ✅ Core Query Function ===
def run_query(question: str) -> str:
    """Generate precise, concise responses to user queries"""
    try:
        logger.info(f"Question: {question}")
        
        # Step 1: Generate SQL
        raw_sql = sql_sequence.invoke({"question": question})
        logger.info(f"Raw SQL: {raw_sql}")
        
        # Handle clarification requests
        if "CLARIFY:" in raw_sql:
            return raw_sql.replace("CLARIFY:", "").strip()
        
        # Clean and validate SQL
        sql_query = clean_sql(raw_sql)
        logger.info(f"Clean SQL: {sql_query}")
        
        if not validate_sql(sql_query):
            return "I need to clarify something about our data. Could you rephrase your question?"
        
        # Step 2: Execute SQL
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()
        
        # Format results
        if rows:
            df = pd.DataFrame(rows, columns=columns)
            result_str = df.to_markdown(index=False)
        else:
            result_str = "No results found"
        logger.info(f"Results: {result_str[:100]}...")
        
        # Step 3: Generate concise response
        response = response_sequence.invoke({
            "question": question,
            "sql": sql_query,
            "result": result_str
        })
        
        # Extract just the concise response
        final_response = response.split("Concise Response:")[-1].strip()
        logger.info(f"Final Response: {final_response}")
        
        return final_response
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "I need more details to answer that. Could you please rephrase?"