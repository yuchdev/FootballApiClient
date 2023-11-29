import argparse
import sys
from football_client.api_client import World


def extract_id(value):
    """
    Extract ID or name from entity identifier
    :param value: identifier to verify
    :return: integer value for ID or original value for name
    """
    entity_id = None
    entity_name = None
    try:
        entity_id = int(value)
    except ValueError:
        entity_name = value
    return entity_id, entity_name


def sanity_check(args):
    """
    Perform sanity check on command-line arguments
    """
    if args.entity in ['league', 'country'] and (args.season or args.league_id):
        print("Warning: --season argument and --league-id is not required for getting global details. Ignoring")
    elif args.entity in ['team', 'player'] and (not args.league_id or not args.season):
        print("Error: --league-id and --season are required for getting team or player details")
        sys.exit(1)


class FootballClientApp:
    """
    CLI for Football API
    """

    def __init__(self, action, entity, serializer):
        self.get_dispatch = {
            'countries': self.all_countries,
            'league': self.get_league,
            'leagues': self.all_leagues,
            'team': self.get_team,
            'player': self.get_player,

        }
        self.action = action
        self.entity = entity
        self.serializer = serializer

    def search(self, **kwargs):
        """
        Run the entity search
        """
        return self.get_dispatch[self.entity](**kwargs)

    def all_leagues(self):
        print(f"Getting leagues information")
        world_leagues = World(serializer=self.serializer)
        result = world_leagues.all_leagues()
        # world_leagues.serialize(entity='leagues', data=result)
        return result

    def all_countries(self):
        print(f"Getting countries information")
        world_leagues = World(serializer=self.serializer)
        result = world_leagues.all_countries()
        world_leagues.serialize(entity='countries', data=result)
        return result

    def get_league(self, identifier):
        print(f"Getting league information for {identifier}")
        entity_id, entity_name = extract_id(identifier)
        world_leagues = World(serializer=self.serializer)
        result = world_leagues.get_league(league_id=entity_id, league_name=entity_name)
        # world_leagues.serialize(entity='league', data=result)
        return result

    def get_team(self, identifier, season=None, league_id=None):
        print(f"Getting team information for {identifier} in season {season}")
        entity_id, entity_name = extract_id(identifier)
        print(f"ID={entity_id}, Name={entity_name}, Season={season}, League ID={league_id}")
        # TODO: get_team() method is not implemented yet
        raise NotImplementedError

    def get_player(self, identifier, season=None, league_id=None):
        print(f"Getting player information for {identifier} in season {season}")
        entity_id, entity_name = extract_id(identifier)
        print(f"ID={entity_id}, Name={entity_name}, Season={season}, League ID={league_id}")
        # TODO: get_player() method is not implemented yet
        raise NotImplementedError


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description='Football API CLI')

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='action', help='Available commands')

    # Command: get
    parser_get = subparsers.add_parser('get', help='Get league, team, or player by ID or name')

    parser_get.add_argument('entity', choices=['league', 'team', 'player'],
                            help='Type of entity to get')
    parser_get.add_argument('identifier',
                            help='ID or name of the entity')
    parser_get.add_argument('--league-id', type=int,
                            help='ID of the league (required for players and teams)')
    parser_get.add_argument('--season', type=int,
                            help='Season year (required for players and teams)')

    # Command: all
    parser_all = subparsers.add_parser('all', help='Get all entities of a type')

    parser_all.add_argument('entity', choices=['countries', 'leagues', 'players', 'teams'],
                            help='Type of entities to get')
    parser_all.add_argument('--league-id', type=int,
                            help='ID of the league (required for players and teams)')
    parser_all.add_argument('--season', type=int,
                            help='Season year (required for players and teams)')
    parser_all.add_argument('--serializer', choices=['json', 'csv'], default='json',
                            help='Output format for the data')

    args = parser.parse_args()
    sanity_check(args)

    # Create a dictionary with non-None values
    print(args)
    kwargs = {
        attr: getattr(args, attr) for attr in ['identifier', 'league_id', 'season']
        if hasattr(args, attr) and getattr(args, attr) is not None
    }
    print(kwargs)
    app = FootballClientApp(action=args.action,
                            entity=args.entity,
                            serializer=args.serializer if hasattr(args, 'serializer') else 'json')
    found_results = app.search(**kwargs)
    if isinstance(found_results, list):
        print(f"Found {len(found_results)} {args.entity}")
    elif isinstance(found_results, dict):
        print(found_results)
    else:
        print("No results found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
