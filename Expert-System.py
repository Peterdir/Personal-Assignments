def checkCondition(condition):
    while True:
        answer = input(f"Hôm nay có {condition} không? (y/n): ")
        answer = answer.strip().lower()

        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Vui lòng nhập 'y/n' hoặc 'yes/no'. Thử lại...")

# Cơ sở tri thức
rules = [
    {
        "conditions": {"exercise": True},
        "conclusion": "Bạn đừng bỏ lỡ bài kiểm tra quan trọng!"
    },
    {
        "conditions": {"raining": True, "sick": True},
        "conclusion": "Bạn nên ở nhà, nếu không bạn sẽ bị cảm nặng hơn!"
    },
    {
        "conditions": {"raining": True},
        "conclusion": "Bạn nên mặc áo mưa vào để đi học."
    },
    {
        "conditions": {"sick": True},
        "conclusion": "Hãy uống thuốc sau đó đi học, cố lên!!!"
    },
    {
        "conditions": {},
        "conclusion": "Hãy đến trường để học được những kiến thức thú vị :)"
    }
]

# Máy suy luận
def inference_engine(facts):
    for rule in rules:
        check = True
        
        for key, value in rule["conditions"].items():
            if(facts.get(key) != value):
                check = False
        if(check):
            return rule["conclusion"]
    return "Không có kết luận phù hợp"

def Determine():

    facts = {
        "raining": checkCondition("mưa"),
        "exercise": checkCondition("bài kiểm tra quan trọng"),
        "sick": checkCondition("cảm lạnh")
    }

    conclusion = inference_engine(facts)
    print(conclusion)

if __name__ == "__main__":
    Determine()