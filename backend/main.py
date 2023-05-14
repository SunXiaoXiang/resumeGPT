from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from redlines import Redlines
from IPython.display import display, Markdown


OPENAI_API_KEY = "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" 
openai.api_key = OPENAI_API_KEY


app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Resume(BaseModel):
    id: str
    age: str
    skills: str
    experiences: str


def summarize_text(text):
    content = f"请对以下文本进行总结，注意总结的凝炼性，将总结字数控制在100个字以内:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": content}],
        temperature=0.3
    )
    summarized_text = response.get("choices")[0].get("message").get("content")
    return summarized_text


def correct_text(text):
    content = f"请对以下文本进行文本纠错:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": content}]
    )
    corrected_text = response.get("choices")[0].get("message").get("content")
    return corrected_text


def complete(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0,
      max_tokens=64,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    ans = response.choices[0].text
    return ans


def ask(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": content}]
    )

    ans = response.get("choices")[0].get("message").get("content")
    return ans

@app.get("/")
async def get_message():
    return {"message": "Hello World!"}


@app.get("/blogs")
async def get_blogs():
    blogs = [
        {
            "title": "My First Blog Post",
            "content": "This is my first blog post.",
        },
        {
            "title": "My Second Blog Post",
            "content": "This is my second blog post.",
        },
    ]
    return blogs


@app.get("/resumes")
async def getresumes():
    resumes = {
        "id": "1",
        "name": "某某某",
        "age": "30",
        "skills": "java, C#, bigdata, python, vue3, js",
        "experiences": '''2019.12 - 至今 |锤子简历科技有限公司|IT技术支持工程师
Helpdesk桌面技术支持与电脑软硬件及周边办公设备的日常维护
IT资产设备的管理，统计T资产相关信息并及时更新资产系统；主要负责T资产台账，维护及更新；IT资产的入库、发放回收、调配、维修、报废等管理工作，并定期配合财务部盘点IT资产
IT设备需求提报，每月定时定点统计库存设备，根据库存量提报相应设备及耗材需求申请ESXI虚拟机的维护及管理。
AD帐户的建立与管理设置;文件服务器的权限分配与设置及重要数据的备份;配合部门其它同事处理紧急事情，及时完成上级分配的任务并反馈信息
协助处理机房服务器的搬迁及搬迁过程中的突发问题及测试；协助处理办公室网络架构的测试，配合无线网络及电话系统的测试
'''}
    return resumes

@app.get("/summary")
async def getsummary():
    text = """2019.12 - 至今 |锤子简历科技有限公司|IT技术支持工程师
Helpdesk桌面技术支持与电脑软硬件及周边办公设备的日常维护
IT资产设备的管理，统计T资产相关信息并及时更新资产系统；主要负责T资产台账，维护及更新；IT资产的入库、发放回收、调配、维修、报废等管理工作，并定期配合财务部盘点IT资产
IT设备需求提报，每月定时定点统计库存设备，根据库存量提报相应设备及耗材需求申请ESXI虚拟机的维护及管理。
AD帐户的建立与管理设置;文件服务器的权限分配与设置及重要数据的备份;配合部门其它同事处理紧急事情，及时完成上级分配的任务并反馈信息
协助处理机房服务器的搬迁及搬迁过程中的突发问题及测试；协助处理办公室网络架构的测试，配合无线网络及电话系统的测试
"""
    output_text = summarize_text(text)

    return {
        "summaryLen": len(output_text),
        "summaryText": output_text }

# 注意，chatgpt并不能完美限制摘要输出的字数


@app.get("/correct")
async def getcorrect():
    text = """2019.12 - 至今 |锤子简历科技有限公司|IT技术支持工程师
Helpdesk桌面技术支持与电脑软硬件及周边办公设备的日常维护
IT资产设备的管理，统计T资产相关信息并及时更新资产系统；主要负责T资产台账，维护及更新；IT资产的入库、发放回收、调配、维修、报废等管理工作，并定期配合财务部盘点IT资产
IT设备需求提报，每月定时定点统计库存设备，根据库存量提报相应设备及耗材需求申请ESXI虚拟机的维护及管理。
AD帐户的建立与管理设置;文件服务器的权限分配与设置及重要数据的备份;配合部门其它同事处理紧急事情，及时完成上级分配的任务并反馈信息
协助处理机房服务器的搬迁及搬迁过程中的突发问题及测试；协助处理办公室网络架构的测试，配合无线网络及电话系统的测试
"""
    output_text = correct_text(text)


    diff = Redlines(' '.join(list(text)),' '.join(list(output_text)))
#    display(Markdown(diff.output_markdown))
    output_text1 = Markdown(diff.output_markdown).data

    return {
        "correctLen": len(output_text),
        "correctText": output_text1 }


@app.get("/entities")
async def showEntities():
        details = """2019.12 - 至今 |锤子简历科技有限公司|IT技术支持工程师
        Helpdesk桌面技术支持与电脑软硬件及周边办公设备的日常维护
        IT资产设备的管理，统计T资产相关信息并及时更新资产系统；主要负责T资产台账，维护及更新；IT资产的入库、发放回收、调配、维修、报废等管理工作，并定期配合财务部盘点IT资产
        IT设备需求提报，每月定时定点统计库存设备，根据库存量提报相应设备及耗材需求申请ESXI虚拟机的维护及管理。
        AD帐户的建立与管理设置;文件服务器的权限分配与设置及重要数据的备份;配合部门其它同事处理紧急事情，及时完成上级分配的任务并反馈信息
        协助处理机房服务器的搬迁及搬迁过程中的突发问题及测试；协助处理办公室网络架构的测试，配合无线网络及电话系统的测试
        """
        prompt = f"""
        请抽取给定Text中的实体，实体是公司名字，按照以下的格式：
        Company：<公司名称>

        Text:{details}"""
        cans = complete(prompt)

        prompt = f"""
        请抽取给定Text中的实体，实体是IT技术名词，按照以下的格式：
        Technology：<IT技术名词>

        Text:{details}"""
        sans = complete(prompt)

        return {"company": cans, 
                "Technology": sans}


@app.get("/searchEntities")
async def searchEntities(company: str ="huawei", skills: str="java"):
        prompt = f"""
        请提供{company}公司的50字简介"""
        cans = ask(prompt)
        prompt = f"""
        请提供{skills}技术的200字简介"""
        sans = ask(prompt)

        return {"companyD": cans, 
                "techD": sans}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
