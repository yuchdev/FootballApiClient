import argparse
import sys
from football_client.api_client import WorldLeagues


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
    if args.entity == 'league' and (args.season or args.league_id):
        print("Warning: --season argument and --league-id is not required for getting league details. Ignoring")
    elif args.entity in ['team', 'player'] and (not args.league_id or not args.season):
        print("Error: --league-id and --season are required for getting team or player details")
        sys.exit(1)


class FootballClientApp:
    """
    CLI for Football API
    """

    def __init__(self, action, entity, identifier, season=None, league_id=None):
        self.get_dispatch = {
            'league': self.get_league,
            'team': self.get_team,
            'player': self.get_player,

        }
        self.action = action
        self.entity = entity
        self.identifier = identifier
        self.season = season
        self.league_id = league_id

    def run(self):
        """
        Run the CLI
        """
        return self.get_dispatch[self.entity](self.action)

    def get_league(self, action):
        print(f"Getting league information for {self.identifier}")
        entity_id, entity_name = extract_id(self.identifier)
        world_leagues = WorldLeagues(serializer="json")
        if action == 'all':
            return world_leagues.all()
        elif action == 'get':
            return world_leagues.get_league(league_id=entity_id, league_name=entity_name)

    def get_team(self, action):
        print(f"Getting team information for {self.identifier} in season {self.season}")
        entity_id, entity_name = extract_id(self.identifier)
        print(f"Action={action}; ID={entity_id}, Name={entity_name}, Season={self.season}, League ID={self.league_id}")
        # TODO: get_team() method is not implemented yet
        raise NotImplementedError

    def get_player(self, action):
        print(f"Getting player information for {self.identifier} in season {self.season}")
        entity_id, entity_name = extract_id(self.identifier)
        print(f"Action={action}; ID={entity_id}, Name={entity_name}, Season={self.season}, League ID={self.league_id}")
        # TODO: get_player() method is not implemented yet
        raise NotImplementedError


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description='Football API CLI')

    # Command: get
    parser.add_argument('action',
                        choices=['get', 'all'],
                        help='Action to perform')
    parser.add_argument('entity',
                        choices=['league', 'team', 'player'],
                        help='Type of entity to get')
    parser.add_argument('identifier',
                        help='ID or name of the entity')
    parser.add_argument('--season',
                        type=int,
                        help='Season year (required for players and teams)')
    parser.add_argument('--league-id',
                        type=int,
                        help='League ID (required for players and teams)')

    # Parse command-line arguments
    args = parser.parse_args()
    sanity_check(args)
    app = FootballClientApp(action=args.action,
                            entity=args.entity,
                            identifier=args.identifier,
                            season=args.season,
                            league_id=args.league_id)
    found = app.run()
    print(found)
    return 0


if __name__ == "__main__":
    sys.exit(main())
