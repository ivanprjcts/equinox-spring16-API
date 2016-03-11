from sdk import DefaultApi


api = DefaultApi()
api.set_proxy("localhost:8080")

api.get_applications()

api.post_applications("app5", True)