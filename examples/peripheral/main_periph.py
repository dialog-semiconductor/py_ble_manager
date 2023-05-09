import argparse
import threading
import queue
import time
# TODO rethink relative import
# TODO rethink relative import
import sys
import python_gtl_thread as ble

'''
from ble.CustomBleService import CustomBleService, CustomBleServiceCallbacks


async def app_char1_read_callback(svc: CustomBleService, conn_idx: int):
    print("app_char1_read_callback")
    data = 0x05
    await svc.send_char1_read_cfm(conn_idx,
                                  ble.ATT_ERROR.ATT_ERROR_OK,
                                  data.to_bytes(1, byteorder='little'))


async def app_char1_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char1_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char1_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)


async def app_char2_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char2_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char2_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)
    await svc.set_char2_value(value.to_bytes(2, byteorder='little'))


async def app_char3_ccc_changed_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char3_ccc_changed_callback. conn_idx={conn_idx}, value={value}")

'''

async def main(com_port: str):

    sample_q = queue.Queue()


    ble_thread = threading.Thread(target=threading.Thread(target=ble_task))
    ble_thread.start()

    while True:
        if ble_thread.is_alive():
            time.sleep(1)
        else:
            return)




async def ble_task(com_port: str, sample_q: queue.Queue):

    periph = ble.BlePeripheral(com_port, gtl_debug=True)
    await periph.init()
    await periph.start()

    #my_service_callbacks = CustomBleServiceCallbacks(app_char1_read_callback,
    #                                                 app_char1_write_callback,
    #                                                 app_char2_write_callback)
    #my_service = CustomBleService(my_service_callbacks)
    #my_service.init()

    #await periph.register_service(my_service)
    #await my_service.set_char2_value((0x8692).to_bytes(2, 'little'))
    #await my_service.set_char3_user_desc_value(b"Hello")

    periph.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_DISP_YES_NO)

    periph.set_advertising_interval(20, 30)
    await periph.start_advertising()

    #timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
    #ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
    #pending = [timer_read_task, ble_event_task]

    while True:
        #done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        evt = periph.get_event()
       
        if evt is not None:
            handled = await periph.service_handle_event(evt)
            if not handled:
                match evt.evt_code:
                    case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                        await periph.start_advertising()
                    case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
                        evt: ble.BleEventGapPairReq
                        print(f"BleEventGapPairReq. evt={evt}")
                        await periph.pair_reply(evt.conn_idx, True, evt.bond)
                    case ble.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST:
                        await periph.numeric_reply(evt.conn_idx, True)
                    case _:
                        await periph.handle_event_default(evt)
           


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central AT Command CLI')

    parser.add_argument("com_port")

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Keyborard")
