"""
工具的媒体输入
=============================

展示工具如何访问传递给 agent 的媒体（图像、视频、音频、文件）。
"""

from typing import Optional, Sequence

from agno.agent import Agent
from agno.media import File
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat  # noqa: F401
from agno.tools import Toolkit


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
class DocumentProcessingTools(Toolkit):
    def __init__(self):
        tools = [
            self.extract_text_from_pdf,
        ]

        super().__init__(name="document_processing_tools", tools=tools)

    def extract_text_from_pdf(self, files: Optional[Sequence[File]] = None) -> str:
        """
        使用 OCR 从上传的 PDF 文件中提取文本。

        此工具可以访问传递给 agent 的任何文件。
        在实际实现中，你应该使用适当的 OCR 服务。

        Args:
            files: 传递给 agent 的文件（自动注入）

        Returns:
            从 PDF 文件提取的文本
        """
        if not files:
            return "未上传任何文件以处理。"

        print(f"--> Files: {files}")

        extracted_texts = []
        for i, file in enumerate(files):
            if file.content:
                # 模拟 OCR 处理
                # 实际上，你应该使用诸如 Tesseract、AWS Textract 等服务
                file_size = len(file.content)
                extracted_text = f"""
                    [文件 {i + 1} 的模拟 OCR 结果]
                    文档处理成功！
                    文件大小: {file_size} 字节

                    提取的示例内容:
                    "这是一份包含季度销售数据重要信息的示例文档。
                    第一季度收入: $125,000
                    第二季度收入: $150,000
                    第三季度收入: $175,000

                    增长趋势显示季度环比增长 20%。"
                """
                extracted_texts.append(extracted_text)
            else:
                extracted_texts.append(
                    f"文件 {i + 1}: 内容为空或无法访问。"
                )

        return "\n\n".join(extracted_texts)


def create_sample_pdf_content() -> bytes:
    """创建用于演示的示例 PDF 样内容。"""
    # 这只是示例二进制内容 - 实际场景中你应该有真实的 PDF 字节
    sample_content = """
    %PDF-1.4
    用于演示的示例 PDF 内容
    在真实场景中这应该是实际的 PDF 二进制数据
    """.encode("utf-8")
    return sample_content


def main():
    # 创建一个具有文档处理工具的 agent
    agent = Agent(
        # model=OpenAIChat(id="gpt-4o"),
        model=Gemini(id="gemini-2.5-pro"),
        tools=[DocumentProcessingTools()],
        name="Document Processing Agent",
        description="一个可以处理上传文档的 agent。使用工具从 PDF 中提取文本。",
        debug_mode=True,
        send_media_to_model=False,
        store_media=True,
    )

    print("=== 工具媒体访问示例 ===\n")

    # 示例 1: PDF 处理
    print("1. 测试 PDF 处理...")

    # 创建示例文件内容
    pdf_content = create_sample_pdf_content()
    sample_file = File(content=pdf_content)

    response = agent.run(
        input="我上传了一份 PDF 文档。请从中提取文本并总结关键财务信息。",
        files=[sample_file],
        session_id="test_files",
    )

    print(f"Agent 响应: {response.content}")
    print("\n" + "=" * 50 + "\n")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
