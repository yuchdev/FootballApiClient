from football_client.json_serializer import JsonSerializer, LeaguesJsonSerializer
from football_client.csv_serializer import CsvSerializer, LeaguesCsvSerializer


class SerializerFactory:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def create_serializer(self, serializer_type, entity):
        serializer_types = {
            "json": JsonSerializer,
            "csv": CsvSerializer,
        }

        entity_serializers = {
            "leagues": {
                "json": LeaguesJsonSerializer,
                "csv": LeaguesCsvSerializer,
            }
            # Add more entity-specific serializers as needed
        }

        entity_serializer_cls = entity_serializers.get(entity, {}).get(serializer_type, None)

        if entity_serializer_cls:
            return entity_serializer_cls(self.data_dir)
        else:
            serializer_cls = serializer_types.get(serializer_type, None)
            if serializer_cls:
                return serializer_cls(self.data_dir, file_name=entity, settings=None)
            else:
                raise ValueError(f"Unsupported serializer or entity: {serializer_type}, {entity}")
