# 要件定義書を生成するクラス
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..data_models.interview import Interview
from .utils import invoke_with_retry


class RequirementsDocumentGenerator:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm

    def run(self, user_request: str, interviews: list[Interview]) -> str:
        # プロンプトを定義
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは収集した情報に基づいて要件文書を作成する専門家です。\n"
                    "要件文書はマークダウン形式で作成して下さい。\n"
                    "ただし、箇条書きか番号付きリスト**のみ**を使用して下さい。\n"
                    "出力は必ず日本語でお願いします。",
                ),
                (
                    "human",
                    "以下のユーザーリクエストと複数のペルソナからのインタビュー結果に基づいて、要件文書を作成してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "インタビュー結果:\n{interview_results}\n"
                    "要件文書には以下のセクションを含めてください:\n"
                    "1. プロジェクト概要\n"
                    "2. 主要機能\n"
                    "3. 非機能要件\n"
                    "4. 制約条件\n"
                    "5. ターゲットユーザー\n"
                    "6. 優先順位\n"
                    "7-1. リスク\n"
                    "7-2. リスクの影響度\n"
                    "8. リスクに対する軽減策",
                ),
            ]
        )
        # 要件定義書を生成するチェーンを作成
        chain = prompt | self.llm | StrOutputParser()
        # 要件定義書を生成
        return invoke_with_retry(
            chain,
            {
                "user_request": user_request,
                "interview_results": "\n".join(
                    f"ペルソナ: {i.persona.name} - {i.persona.background}\n"
                    f"質問: {i.question}\n回答: {i.answer}\n"
                    for i in interviews
                ),
            },
        )
