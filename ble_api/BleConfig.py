from gtl_port.gap import GAP_KDIST


dg_configBLE_DATA_LENGTH_TX_MAX = (251)
dg_configBLE_SECURE_CONNECTIONS = (1)
dg_configBLE_PAIR_INIT_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
dg_configBLE_PAIR_RESP_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
dg_configBLE_PRIVACY_1_2 = (0)
dg_configBLE_CENTRAL = (1)
dg_configBLE_PERIPHERAL = (0) # need to be careful for different 
dg_configBLE_DATA_LENGTH_RX_MAX = (251)
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


def ble_data_length_to_time(OCTETS):
    return (OCTETS + 11 + 3) * 8
