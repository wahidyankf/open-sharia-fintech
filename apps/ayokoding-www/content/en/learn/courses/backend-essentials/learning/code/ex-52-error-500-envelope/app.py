"""Example 52: A Sanitized 500 Envelope for Unhandled Exceptions."""

# => co-11: the /boom handler below ALWAYS raises -- real uvicorn+curl gets
#    the sanitized JSON below; the raw exception detail only ever reaches server logs
from fastapi import FastAPI, Request  # => Request gives the handler access to the raw ASGI request
from fastapi.responses import JSONResponse  # => the response type this handler builds by hand

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.exception_handler(Exception)  # => co-11: catches EVERYTHING not already handled elsewhere
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,  # => exc is the ORIGINAL exception, never shown to the caller
) -> JSONResponse:  # => must return a Response FastAPI can send back to the client
    # => deliberately generic -- never leaks exc's message or a stack trace to the client;
    #    a real deployment would log str(exc) SERVER-SIDE here, just never return it
    return JSONResponse(  # => builds the sanitized envelope BY HAND, replacing the raw traceback
        status_code=500,  # => co-03: server-side failure
        content={  # => the JSON body FastAPI serializes and sends back to the client
            "error": {  # => nests everything under ONE top-level key, matching earlier envelopes
                "code": "internal_error",  # => a stable, machine-matchable code
                "message": "an unexpected error occurred",  # => deliberately generic, every time
            }  # => closes the inner "error" object
        },  # => closes the "content" dict passed to JSONResponse
    )  # => closes the JSONResponse(...) call itself


@app.get("/boom")  # => co-08: a handler that always fails, on purpose, for this example
def boom() -> None:  # => never returns normally -- exists solely to trigger the handler above
    raise RuntimeError(  # => co-11: an ORDINARY, unhandled exception -- not a domain error
        "something exploded with sensitive internal details"  # => never reaches the client
    )  # => this string never reaches the client -- the handler above replaces it entirely
