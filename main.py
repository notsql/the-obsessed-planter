import serial as s
import configparser as cfg
from time import sleep

AT_COMMANDS = {
  "status": b"AT\r\n",
  "model_id": b"AT+CGMM\r\n",
  "model_sn": b"AT+CGSN\r\n",
  "module": b"AT+CSUB\r\n",
  "sim_id": b"AT+CICCID\r\n",
  "sim_no": b"AT+CNUM\r\n",
  "sim_op": b"AT+COPS?\r\n"
}

def load_configs():
  config = cfg.RawConfigParser()
  config.read("./config.cfg")

  app_config = dict(config.items("app"))
  gsm_config = dict(config.items("gsm"))

  return dict(
    app=app_config,
    gsm=gsm_config)

def get_res(gsm, command):
  gsm.write(command)

  buffer = gsm.readline()
  sleep(0.1)
  buffer += gsm.read(gsm.in_waiting)

  return buffer.decode().split("\n")[1]


def init_gsm(port, baudrate, bytesize, stopbits, debug):
  try:
    gsm = s.Serial(
      port=port,
      baudrate=baudrate,
      bytesize=bytesize,
      stopbits=stopbits
    )
  except:
    gsm = AssertionError("Unable to load GSM")

  gsm.flush()

  if debug:
    print("\n", "***GSM Information***")
    print("Status:\t\t", get_res(gsm, AT_COMMANDS["status"]))
    print("Model ID:\t", get_res(gsm, AT_COMMANDS["model_id"]))
    print("Model SN.:\t", get_res(gsm, AT_COMMANDS["model_sn"]))
    print("Module:\t\t", get_res(gsm, AT_COMMANDS["module"]))

    print("\n", "***SIM Informaiton***")
    print("Carrier:\t", get_res(gsm, AT_COMMANDS["sim_op"]))
    print("SIM ID:\t\t", get_res(gsm, AT_COMMANDS["sim_id"]))
    print("Phone No.:\t", get_res(gsm, AT_COMMANDS["sim_no"]))

  return gsm

def main():
  config = load_configs()

  gsm = init_gsm(
    config["gsm"]["port"],
    int(config["gsm"]["baudrate"]),
    int(config["gsm"]["bytesize"]),
    int(config["gsm"]["stopbits"]),
    bool(config["app"]["debug"])
  )

  gsm.close()

if __name__ == "__main__":
  main()