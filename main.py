
import json
import WLAN
from machine import Pin
from neopixel import NeoPixel
from microdot import Microdot, redirect

AP = 110
WIFI = 111

CONFIG = json.load(open("config.json"))
pin = Pin(CONFIG["pin"])
ws2812 = NeoPixel(pin, CONFIG["number"])
wlan = WLAN.WLAN()
app = Microdot()


def fill_color(color):
	for light in range(CONFIG["number"]):
		ws2812[light] = color


def init_wlan():
	if not CONFIG["ssid"]:
		wlan.ap_active(True)
		wlan.set_ap_config("fillLight", "12345678")
		wlan.ap_ifconfig(("192.168.10.1", "255.255.255.0", "192.168.10.1", "114.114.114.114"))
	else:
		wlan.wifi_active(True)
		while not wlan.isconnected():
			wlan.connect_wifi(CONFIG["ssid"], CONFIG["passwd"])


@app.get("/")
def index(req):
	return open("index.html").read(), 200, {'Content-Type': 'text/html'}


@app.post("/set")
def set(req):
	if req.form.get("on"):
		color = (int(req.form.get("r")), int(req.form.get("g")), int(req.form.get("b")))
		print(color)
		fill_color(color)
	else:
		fill_color((0, 0, 0))
	CONFIG["ssid"] = req.form.get("ssid")
	CONFIG["passwd"] = req.form.get("passwd")
	json.dump(CONFIG, open("config.json", "w"))
	return redirect("/")


def main():
	fill_color((0, 0, 0))
	for light in range(0, CONFIG["number"], 8):
		ws2812[light + 3] = (255, 255, 255)
		ws2812[light + 4] = (255, 255, 255)

	init_wlan()
	app.run("0.0.0.0", 80)


if __name__ == "__main__":
	main()
