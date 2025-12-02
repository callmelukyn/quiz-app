from fastapi import HTTPException, Request

def register_error_pages(app, templates):
    @app.exception_handler(404)
    async def redirect_to_404_html(request: Request, _exc: HTTPException):
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    @app.exception_handler(405)
    async def redirect_to_403_html(request: Request, _exc: HTTPException):
        return templates.TemplateResponse("405.html", {"request": request}, status_code=405)

    @app.exception_handler(500)
    async def redirect_to_500_html(request: Request, _exc: HTTPException):
        return templates.TemplateResponse("404.html", {"request": request}, status_code=500)