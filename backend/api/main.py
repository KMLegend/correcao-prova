import json
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from adapters.opencv_extractor import OpenCVAnswerExtractor
from api.validators import FileValidator, FileValidationError
from domain.entities import Answer, AnswerSheet, CorrectionResult
from domain.value_objects import AnswerChoice, QuestionNumber
from use_cases.evaluate_exam import EvaluateExamUseCase


app = FastAPI(
    title="Sistema de Correção Automática de Provas",
    description="API para correção automática de cartões-resposta usando OCR/OMR.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = OpenCVAnswerExtractor()
use_case = EvaluateExamUseCase(extractor)
file_validator = FileValidator()


@app.get("/")
async def root():
    return {"message": "Sistema de Correção Automática de Provas - API Online"}


@app.post("/corrigir")
async def corrigir_prova(
    gabarito: UploadFile = File(..., description="Imagem do gabarito oficial"),
    cartao: UploadFile = File(..., description="Imagem do cartão-resposta do aluno"),
):
    """Endpoint principal: recebe gabarito e cartão-resposta, retorna correção."""
    file_validator.validate(gabarito)
    file_validator.validate(cartao)

    gabarito_bytes = await gabarito.read()
    cartao_bytes = await cartao.read()

    await file_validator.validate_size(gabarito_bytes)
    await file_validator.validate_size(cartao_bytes)

    try:
        results = use_case.execute(gabarito_bytes, cartao_bytes)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    return _format_response(results)


@app.post("/corrigir-com-json")
async def corrigir_com_gabarito_json(
    gabarito_json: str = File(..., description="JSON do gabarito no formato {questao: resposta}"),
    cartao: UploadFile = File(..., description="Imagem do cartão-resposta do aluno"),
):
    """Endpoint alternativo: recebe gabarito em JSON e cartão-resposta como imagem."""
    file_validator.validate(cartao)
    cartao_bytes = await cartao.read()
    await file_validator.validate_size(cartao_bytes)

    try:
        answer_key_sheet = _parse_json_answer_key(gabarito_json)
        results = use_case.execute_with_json_key(answer_key_sheet, cartao_bytes)
    except (ValueError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=422, detail=str(error))

    return _format_response(results)


def _parse_json_answer_key(json_string: str) -> AnswerSheet:
    """Converte JSON de gabarito para AnswerSheet.

    Formato esperado: {"1": "A", "2": "B", "3": "C", ...}
    """
    data = json.loads(json_string)
    answers: List[Answer] = []
    for question_str, choice_str in data.items():
        question = QuestionNumber(int(question_str))
        choice = AnswerChoice(choice_str)
        answer = Answer(question, choice)
        answers.append(answer)
    return AnswerSheet(answers)


def _format_response(results: List[CorrectionResult]) -> dict:
    """Formata a resposta da correção para JSON."""
    total = len(results)
    acertos = sum(1 for r in results if r.is_correct())
    erros = total - acertos
    nota = (acertos / total * 10) if total > 0 else 0

    return {
        "resumo": {
            "total_questoes": total,
            "acertos": acertos,
            "erros": erros,
            "nota": round(nota, 1),
        },
        "detalhes": [result.to_dict() for result in results],
    }
