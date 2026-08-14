'''from fastapi import APIRouter, UploadFile, File, HTTPException 
import pandas as pd
from database.database import get_connection

#APIRouter :Allows us to group related endpoints.
#UploadFile :Represents an uploaded file.
#File :Tells FastAPI:This parameter comes from a file upload.
#HTTPException :Allows us to return proper HTTP errors.

router = APIRouter(
    prefix="/upload",
    tags=["Dataset"]
)


@router.post("/dataset")
async def upload_dataset(
    file: UploadFile = File(...)
):
    """
    Upload a CSV dataset and store it in SQLite.
    """

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."       #if a pdf or any other file is uploaded it will return 400 HTTPerror
        )

    try:

        df = pd.read_csv(file.file)

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded dataset is empty."
            )

        connection = get_connection()  # if it is not empty then connect to SQLite

        df.to_sql(
            "dataset",
            connection,
            if_exists="replace",
            index=False
        )

        connection.close()   # we will convert dataframe to SQL table

        return {
            "message": "Dataset uploaded successfully.",
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }

    except pd.errors.EmptyDataError:

        raise HTTPException(
            status_code=400,
            detail="The CSV file is empty."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process dataset: {str(e)}"
        )'''

#new

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

import pandas as pd

from database.database import get_connection

router = APIRouter(

    prefix="/upload",

    tags=["Dataset"]
)


@router.post("/dataset")

async def upload_dataset(

    file: UploadFile = File(...)
):

    if not file.filename.endswith(".csv"):

        raise HTTPException(

            status_code=400,

            detail="Only CSV files are supported."
        )

    df = pd.read_csv(file.file)

    connection = get_connection()

    df.to_sql(

        "dataset",

        connection,

        if_exists="replace",

        index=False
    )

    connection.close()

    return {

        "rows": len(df),

        "columns": list(df.columns)
    }