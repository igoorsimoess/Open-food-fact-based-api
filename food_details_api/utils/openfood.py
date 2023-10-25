from openfoodfacts import API, APIVersion, Country, Environment, Flavor
from datetime import datetime


class FoodData:
    def __init__(self, product: str) -> None:
        self.product = product

    def get_data(self) -> dict:
        api = API(
            username=None,
            password=None,
            country=Country.world,
            flavor=Flavor.off,
            version=APIVersion.v2,
            environment=Environment.org,
        )
        info = api.product.get(self.product)
        if "no code or invalid code" in info["status_verbose"]:
            return None

        info = info["product"]
        time_now = datetime.utcnow()
        formatted_time = time_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "code": info.get("code"),  # db
            "imported_t": formatted_time,
            "creator": info.get("creator"),
            "created_t": info.get("created_t"),
            "url": f"https://world.openfoodfacts.org/product/{self.product}",
            "last_modified_t": info.get("last_modified_t"),
            "product_name": info.get("product_name_pt"),  # tratar
            "quantity": info.get("quantity"),
            "brands": info.get("brands"),
            "categories": info.get("categories"),
            "labels": info.get("labels"),
            "cities": None,  # filled by API
            "purchase_places": info.get("countries"),
            "stores": info.get("stores"),
            "ingredients_text": info.get("ingredients_text_pt"),
            "traces": info.get("traces"),
            "serving_size": info.get("serving_size"),
            "serving_quantity": info.get("serving_quantity"),
            "nutriscore_score": info.get("score"),
            "nutriscore_grade": info.get("grade"),
            "main_category": info["categories_hierarchy"][0]
            if "categories_hierarchy" in info
            else None,
            "image_url": info.get("image_url"),
        }
        for key, value in data.items():
            if value == "":
                data[key] = None
        return data
