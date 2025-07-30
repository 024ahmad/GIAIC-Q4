from connection import config
from agents import Agent, Runner, function_tool
import requests


# 🧠 Function tool for nike products filtering
@function_tool
def get_product_data(product: str = None, category: str = None, price: int = None):
    print("🛍️ Shopping Agent is running...")
    print("Nike Product Function Calling")

    # 📡 API call
    response = requests.get("https://template-03-api.vercel.app/api/products")
    data = response.json()["data"]
    filtered = []

    for item in data:
        filtered.append(f"{item['productName']} | Rs.{item['price']} | {item['category']}")

    if not filtered:
        return "📦 Koi product nahi mila."

    return "\n".join(filtered)

# 🧠 Function tool for home products filtering
@function_tool
def get_furniture_products(product_name: str = None, category: str = None, price: int = None):
    print("🛍️ Shopping Agent is running...")
    print("Home Product Function Calling")
    print(f"Name : {product_name}, Category : {category}, Price : {price}")
    # # 📡 API call
    # response = requests.get("https://hackathon-apis.vercel.app/api/products")
    # data = response.json()
    # filtered = []

    # for item in data:
    #     filtered.append(f"{item['name']} | Rs.{item['price']} | {item['category']}")

    # if not filtered:
    #     return "📦 Koi product nahi mila."

    # return "\n".join(filtered)

    url_1 = "https://hackathon-apis.vercel.app/api/products"
    url_2 = "https://next-ecommerce-template-4.vercel.app/api/product"

    data_1 = requests.get(url_1).json()  # assume .json() gives list
    print(f"Data_1 : {data_1}")
    data_2 = requests.get(url_2).json()["products"]
    # print(f"Data_1 : {data_2}")

    combined_data = []

    # Normalize API 1
    for item in data_1:
        combined_data.append({
            "name": item.get("name"),
            "price": item.get("price"),
            "category": item.get("category")
        })

    # print(f"Combined Data : {combined_data}")

    # Normalize API 2
    for item in data_2:
        combined_data.append({
            "name": item.get("name"),
            "price": item.get("price"),
            "category": item.get("category") # .get("name")
        })

    # Now filter based on input
    results = []
    for item in combined_data:
        results.append(f"{item['name']} | Rs.{item['price']} | {item['category']}")

    if not results:
        return "📦 Koi product nahi mila."

    return "\n".join(results)

# 🧠 Function tool for nike products filtering
@function_tool
def get_product_data(product: str = None, category: str = None, price: int = None):
    print("🛍️ Shopping Agent is running...")

    # 📡 API call
    response = requests.get("https://template-03-api.vercel.app/api/products")
    data = response.json()["data"]
    filtered = []

    for item in data:
        filtered.append(f"{item['productName']} | Rs.{item['price']} | {item['category']}")

    if not filtered:
        return "📦 Koi product nahi mila."

    return "\n".join(filtered)

# # 🧠 Function tool for nike products filtering
# @function_tool
# def get_product_data(product: str = None, category: str = None, price: int = None):
#     print("🛍️ Shopping Agent is running...")

#     # 📡 API call
#     response = requests.get("https://template-03-api.vercel.app/api/products")
#     data = response.json()["data"]
#     filtered = []

#     for item in data:
#         filtered.append(f"{item['productName']} | Rs.{item['price']} | {item['category']}")

#     if not filtered:
#         return "📦 Koi product nahi mila."

#     return "\n".join(filtered)

# 🧠 Agent setup
agent = Agent(
    name="Shopping Agent",
    instructions="""You are a helpful shopping assistant. Your job is to help the user find the most relevant products from an online store.

    When the user asks for products, extract details like product name, category, price, brand, or year if provided. Then call the provided function tool to fetch matching data.

    Always present results in a clean, numbered list like:

    Product Name — Rs. Price
    • Category: ...
    • Brand: ...
    • Year: ...

    If no matching product is found, politely inform the user.

    Only show products that meet all user criteria. Be concise but detailed in your answers.
    """, # this is persona, system or user prompt
    tools=[get_product_data,get_furniture_products]
)

# ▶️ Run agent with prompt
result = Runner.run_sync(
    agent,
    "sofa set or chair search kro under 1000 ",  
    run_config=config
)

# 🖨️ Output
print(result.final_output)
