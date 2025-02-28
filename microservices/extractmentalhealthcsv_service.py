from fastapi import APIRouter, HTTPException
from models.generated_models.Extractmentalhealthcsv import ExtractmentalhealthcsvInput, ExtractmentalhealthcsvOutput
import importlib.util
import os
from pathlib import Path

router = APIRouter()

MODELS_DIR = Path("models/generated_models").resolve()

def dynamic_import_function(module_path, function_name):
    """Dynamically import a function from a generated model.""" 
    spec = importlib.util.spec_from_file_location("generated_model", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    available_functions = [attr for attr in dir(module) if callable(getattr(module, attr))]
    print(f"🔍 Available functions in {module_path}: {available_functions}")
    
    return getattr(module, function_name, None)


@router.post("/extractmentalhealthcsv_service/extractmentalhealthcsv")
def process_extractmentalhealthcsv(data: ExtractmentalhealthcsvInput):
    """Dynamically execute extractMentalHealthCSV from generated models.""" 
    model_path = MODELS_DIR / "Extractmentalhealthcsv.py"

    function_to_call = dynamic_import_function(str(model_path), "extractMentalHealthCSV")
    if function_to_call:
        print(f"✅ Function extractMentalHealthCSV found in: {model_path}")
        result = function_to_call(**data.dict())  # Pass Pydantic model data as function arguments
        return ExtractmentalhealthcsvOutput(result=result)

    raise HTTPException(status_code=404, detail="Function 'extractMentalHealthCSV' not found in generated models")