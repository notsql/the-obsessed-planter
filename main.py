import serial as s
import configparser as cfg
from time import sleep

AT_COMMANDS = {
  "status": b"AT\r",
  "model_id": b"AT+CGMM\r",
  "model_sn": b"AT+CGSN\r",
  "module": b"AT+CSUB\r",
  "sim_id": b"AT+CICCID\r",
  "sim_no": b"AT+CNUM\r",
  "sim_op": b"AT+COPS?\r"
}

def load_configs():
  config = cfg.RawConfigParser()
  config.read("./config.cfg")

  app_config = dict(config.items("app"))
  gsm_config = dict(config.items("gsm"))

  return dict(
    app=app_config,
    gsm=gsm_config)

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
    gsm.write(AT_COMMANDS["status"])

    sleep(0.3)

    res = gsm.read()
    res += gsm.read(gsm.in_waiting)

    print(res.decode())

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