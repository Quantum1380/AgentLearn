from langchain_core.runnables import RunnableLambda

# 定义一个普通函数
def add_ten(x: int) -> int:
    return x + 10

def multiply_ten(x: int) -> int:
    return x * 10
# 链接两个 Runnable
chain = RunnableLambda(add_ten) | RunnableLambda(multiply_ten)

result = chain.invoke(1)  # (1 + 10) * 10 = 110

print(result)