import asyncio
import random
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3

class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2

@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: Optional[int] = None

async def get_application_status1(identifier: str) -> Response:
    # Имитация задержки
    await asyncio.sleep(random.uniform(0.1, 0.5))
    # Случайный выбор результата
    return random.choice([Response.Success, Response.RetryAfter, Response.Failure])

async def get_application_status2(identifier: str) -> Response:
    # Имитация задержки
    await asyncio.sleep(random.uniform(0.1, 0.5))
    # Случайный выбор результата
    return random.choice([Response.Success, Response.RetryAfter, Response.Failure])

async def perform_operation(identifier: str) -> ApplicationResponse:
    start_time = datetime.now()
    tasks = [get_application_status1(identifier), get_application_status2(identifier)]
    done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    for task in done:
        response = task.result()
        if response == Response.Success:
            return ApplicationResponse(
                application_id=identifier,
                status=ApplicationStatusResponse.Success,
                description="Operation succeeded",
                last_request_time=datetime.now()
            )
    
    # Если все задачи завершились неудачей
    return ApplicationResponse(
        application_id=identifier,
        status=ApplicationStatusResponse.Failure,
        description="Operation failed",
        last_request_time=datetime.now(),
        retriesCount=len(done)  # Пример, как можно использовать retriesCount
    )

async def main():
    identifier = "12345"
    result = await perform_operation(identifier)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

