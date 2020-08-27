
import logging
import common
from examples import payload_templates as templates
import yaml
import pkgutil

logger = logging.getLogger('main.examples')


def get_module_definition():
    data = pkgutil.get_data(__package__, 'module')
    return yaml.load(data, Loader=yaml.SafeLoader)


def create_global_credentials(api, workflow_dict):
    """ Creates DNA Center Global Credentials.

    :param api: An instance of the dnacentersdk.DNACenterAPI class
    :param workflow_dict: A dictionary containing rows credential definitions (cli, snmp-ro/rw) (see schema.yaml);

    :returns: Nothing """

    _schema = 'snmpWrite.schema.examples'
    logger.info('examples::create_global_credentials::snmpWrite')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        # Cycle through the rows and create entries with 'present' set
        for row in table_data:
            if row['presence']:
                if 'present' in row['presence']:
                    _creds = api.network_discovery.get_global_credentials('SNMPV2_WRITE_COMMUNITY')
                    _id = common.get_object_id(_creds['response'], description=row['description'])
                    if _id is not None:
                        logger.info('SNMPV2_WRITE_COMMUNITY exists with id: {}'.format(_id))
                    else:
                        logger.info('Creating SNMPV2_WRITE_COMMUNITY')
                        result = api.network_discovery.create_snmp_write_community(payload=[common.dot_to_json(row)])
                        logger.debug(result)
    else:
        logger.error('schema not found: {}'.format(_schema))

    _schema = 'snmpRead.schema.examples'
    logger.info('examples::create_global_credentials::snmpRead')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        for row in table_data:
            if row['presence']:
                if 'present' in row['presence']:
                    _creds = api.network_discovery.get_global_credentials('SNMPV2_READ_COMMUNITY')
                    _id = common.get_object_id(_creds['response'], description=row['description'])
                    if _id is not None:
                        logger.info('SNMPV2_READ_COMMUNITY exists with id: {}'.format(_id))
                    else:
                        logger.info('Creating SNMPV2_READ_COMMUNITY')
                        result = api.network_discovery.create_snmp_read_community(payload=[common.dot_to_json(row)])
                        logger.debug(result)
    else:
        logger.error('schema not found: {}'.format(_schema))

    _schema = 'cli.schema.examples'
    logger.info('examples::create_global_credentials::cli')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        for row in table_data:
            if row['presence']:
                if 'present' in row['presence']:
                    _creds = api.network_discovery.get_global_credentials('CLI')
                    _id = common.get_object_id(_creds['response'], description=row['description'])
                    if _id is not None:
                        logger.info('CLI exists with id: {}'.format(_id))
                    else:
                        logger.info('Creating CLI credentials for username: {}'.format(row['username']))
                        result = api.network_discovery.create_cli_credentials(payload=[common.dot_to_json(row)])
                        logger.debug(result)
    else:
        logger.error('schema not found: {}'.format(_schema))


def delete_global_credentials(api, workflow_dict):
    """ Deletes DNA Center Global Credentials based on input from workflow_dict.

    :param api: An instance of the dnacentersdk.DNACenterAPI class
    :param workflow_dict: A dictionary containing rows of credential definitions (cli, snmp-ro/rw) (see schema.yaml);

    :returns: Nothing """

    _schema = 'snmpWrite.schema.examples'
    logger.info('examples::delete_global_credentials::snmpWrite')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        # Cycle through the rows and create entries with 'present' set
        for row in table_data:
            if 'absent' in row['presence'] and 'writeCommunity' in row.keys():
                _creds = api.network_discovery.get_global_credentials('SNMPV2_WRITE_COMMUNITY')
                _id = common.get_object_id(_creds['response'], description=row['description'])
                if _id is not None:
                    logger.info('Deleting SNMPV2_WRITE_COMMUNITY with id: {}'.format(_id))
                    api.network_discovery.delete_global_credentials_by_id(_id)
                else:
                    logger.info('SNMPV2_WRITE_COMMUNITY with description "{}" does not exist'.format(_id))
    else:
        logger.error('schema not found: {}'.format(_schema))

    _schema = 'snmpRead.schema.examples'
    logger.info('examples::delete_global_credentials::snmpRead')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        for row in table_data:
            if 'absent' in row['presence'] and 'readCommunity' in row.keys():
                _creds = api.network_discovery.get_global_credentials('SNMPV2_READ_COMMUNITY')
                _id = common.get_object_id(_creds['response'], description=row['description'])
                if _id is not None:
                    logger.info('Deleting SNMPV2_READ_COMMUNITY with id: {}'.format(_id))
                    api.network_discovery.delete_global_credentials_by_id(_id)
                else:
                    logger.info('SNMPV2_READ_COMMUNITY with description "{}" does not exist'.format(_id))
    else:
        logger.error('schema not found: {}'.format(_schema))

    _schema = 'cli.schema.examples'
    logger.info('examples::delete_global_credentials::cli')
    logger.debug('schema: {}'.format(_schema))

    if _schema in workflow_dict.keys():
        table_data = workflow_dict[_schema]

        for row in table_data:
            if 'absent' in row['presence'] and 'username' in row.keys():
                _creds = api.network_discovery.get_global_credentials('CLI')
                _id = common.get_object_id(_creds['response'], description=row['description'])
                if _id is not None:
                    logger.info('Deleting CLI with id: {}'.format(_id))
                    api.network_discovery.delete_global_credentials_by_id(_id)
                else:
                    logger.info('CLI with description "{}" does not exist'.format(_id))
    else:
        logger.error('schema not found: {}'.format(_schema))


def list_id_groups(api, workflow_dict):
    """ Prints out a list of ISE ID groups.

    :param api: An instance of the ISE SDK class
    :param workflow_dict: A dictionary containing rows of example data (see module);

    :returns: Nothing """

    _schema = None
    logger.info('examples::list_id_groups')
    logger.debug('schema: {}'.format(_schema))

    id_groups = api.get_identity_groups()['response']

    for id_group in id_groups:
        output = 'name: {}, uuid: {}, description: {}'.format(id_group[0], id_group[1], id_group[2])
        print(output.center(len(output) + 10))
