# 情報の十分性を評価するクラス
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


from ..data_models.evaluation import EvaluationResult
from ..data_models.interview import Interview
from .utils import invoke_with_retry


class InformationEvaluator:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm.with_structured_output(EvaluationResult)

    # ユーザーリクエストとインタビュー結果を基に情報の十分性を評価
    def run(self, user_request: str, interviews: list[Interview]) -> EvaluationResult:
        # プロンプトを定義
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは包括的な要件文書を作成するための情報の十分性を評価する専門家です。",
                ),
                (
                    "human",
                    "以下のユーザーリクエストとインタビュー結果に基づいて、包括的な要件文書を作成するのに十分な情報が集まったかどうかを判断してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "インタビュー結果:\n{interview_results}",
                ),
            ]
        )
        # 情報の十分性を評価するチェーンを作成
        chain = prompt | self.llm
        # 評価結果を返す
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
