from aiohttp import web
from app.product.product import Product
import json

routes = web.RouteTableDef()


@routes.post('/api/{method}')
async def handle(request):
    if request.match_info['method'] == 'registerProduct':
        body = await request.post()
        result = await Product.register_product(body["name"], body["secret"])
        return web.Response(text=json.dumps(result))


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app)
