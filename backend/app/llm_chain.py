# backend/app/llm_chain.py

import os
import re
import logging
from sqlalchemy import create_engine, text, inspect
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
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

# === ✅ Data Dictionary ===
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
    temperature=0.1,  # Slightly higher for better creativity
    model_name="llama3-70b-8192",  # More powerful model
    api_key=os.environ["GROQ_API_KEY"]
)

# === ✅ SQL Generation Prompt ===
SQL_PROMPT = PromptTemplate(
    input_variables=["question", "table_info"],
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
""".strip()
).partial(data_dictionary=DATA_DICTIONARY)

# === ✅ Response Generation Prompt ===
RESPONSE_PROMPT = PromptTemplate(
    input_variables=["question", "sql", "result"],
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
""".strip()
).partial(data_dictionary=DATA_DICTIONARY)

# === ✅ Chains ===
sql_chain = LLMChain(llm=llm, prompt=SQL_PROMPT, output_key="sql")
response_chain = LLMChain(llm=llm, prompt=RESPONSE_PROMPT, output_key="response")

# === ✅ Helper Functions ===
def get_table_info():
    """Get schema information for all tables with detailed column info"""
    inspector = inspect(engine)
    table_info = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Create detailed column info: name (type)
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

# === ✅ Core Query Function ===
def run_query(question: str) -> str:
    """Generate precise, concise responses to user queries"""
    try:
        logger.info(f"Question: {question}")
        table_info = get_table_info()
        
        # Step 1: Generate SQL
        sql_result = sql_chain.invoke({"question": question, "table_info": table_info})
        raw_sql = sql_result["sql"].strip()
        logger.info(f"Raw SQL: {raw_sql}")
        
        # Handle clarification requests
        if "CLARIFY:" in raw_sql:
            return raw_sql.replace("CLARIFY:", "").strip()
        
        # Clean and validate SQL
        sql_query = clean_sql(raw_sql)
        logger.info(f"Clean SQL: {sql_query}")
        
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
        response = response_chain.invoke({
            "question": question,
            "sql": sql_query,
            "result": result_str
        })
        
        # Extract just the concise response
        final_response = response["response"].split("Concise Response:")[-1].strip()
        logger.info(f"Final Response: {final_response}")
        
        return final_response
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "I need more details to answer that. Could you please rephrase?"