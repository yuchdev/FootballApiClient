# football_cli.py
import argparse
from api_client import WorldLeagues


def verify_int(value):
    """
    Verify that the value is an integer
    :param value: value to verify
    :return: integer value or original value
    """
    try:
        return int(value)
    except ValueError:
        return value


def validate_id(identifier):
    """
    Validate and return ID or None
    """
    identifier = verify_int(identifier)
    return int(identifier) if isinstance(identifier, int) else None


def validate_name(identifier):
    """
    Validate and return name or None
    """
    identifier = verify_int(identifier)
    return identifier if isinstance(identifier, str) else None


def get_entity(league, entity_type, identifier, season=None):
    """
    Get league, team, or player by ID or name
    :param league:
    :param entity_type:
    :param identifier:
    :param season:
    :return:
    """
    id_value = validate_id(identifier)
    name_value = validate_name(identifier)

    if entity_type == 'league':
        print(f"Getting league information for {id_value or name_value}")
        # Implement logic to get league details
    elif entity_type == 'team':
        print(f"Getting team information for {id_value or name_value} in season {season}")
        league.get_team(season, id=id_value, name=name_value)
    elif entity_type == 'player':
        print(f"Getting player information for {id_value or name_value} in season {season}")
        league.get_player(season, id=id_value, name=name_value)
    else:
        print(f"Invalid entity type: {entity_type}")


def get_all_entities(league, entity_type, league_id=None, season=None):
    if entity_type == 'leagues':
        print("Getting all leagues")
        # Implement logic to get all leagues
    elif entity_type == 'teams':
        print(f"Getting all teams in league {league_id} during season {season}")
        league.get_teams(season)
    elif entity_type == 'players':
        print(f"Getting all players in league {league_id} during season {season}")
        league.get_players(season)
    else:
        print(f"Invalid entity type: {entity_type}")


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description='Football API CLI')

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: get
    parser_get = subparsers.add_parser('get', help='Get league, team, or player by ID or name')

    parser_get.add_argument('type',
                            choices=['league', 'team', 'player'],
                            help='Type of entity to get')
    parser_get.add_argument('identifier',
                            help='ID or name of the entity')
    parser_get.add_argument('--season',
                            type=int,
                            help='Season year (required for players and teams)')

    # Command: all
    parser_all = subparsers.add_parser('all',
                                       help='Get all leagues, players in a league during a specific season, '
                                            'or teams in a league during a specific season')

    parser_all.add_argument('type',
                            choices=['leagues', 'players', 'teams'],
                            help='Type of entities to get')
    parser_all.add_argument('--league-id',
                            type=int,
                            help='ID of the league (required for players and teams)')
    parser_all.add_argument('--season',
                            type=int,
                            help='Season year (required for players and teams)')

    # Parse command-line arguments
    args = parser.parse_args()

    # Initialize WorldLeagues with the JsonSerializer
    world_leagues = WorldLeagues(serializer='json')

    # Execute the selected command
    if args.command == 'get':
        league = world_leagues.by_id(args.identifier)
        if not league:
            print(f"League with ID {args.identifier} not found.")
        else:
            get_entity(league, args.type, args.identifier, args.season)
    elif args.command == 'all':
        get_all_entities(world_leagues, args.type, args.league_id, args.season)


if __name__ == "__main__":
    main()
