# import argparse
# from pythonosc import dispatcher, osc_server
# from eeg_csv import *
#
#
# def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("EEG per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('EEG', values)
#     write_data('raw')
#
#
# def alpha_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("Alpha amp per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('alpha', values)
#
#
# def beta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("Beta amp per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('beta', values)
#
#
# def gamma_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("Gamma amp per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('gamma', values)
#
#
# def delta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("Delta amp per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('delta', values)
#
#
# def theta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#     # print("Theta amp per channel: ", ch1, ch2, ch3, ch4)
#     values = (ch1, ch2, ch3, ch4)
#     update_data('theta', values)
#     write_data('fft')
#
#
# # def jaw_handler(unused_addr, args, ch1):
# #     # print("Jaw clench? : ", ch1)
#
#
# def osc_stream(ip_address="0.0.0.0", port=5000):
#     print('======== INIT OSC STREAM ========')
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", default=ip_address)
#     parser.add_argument("--port", default=port)
#     args = parser.parse_args()
#     global dispatcher
#     dispatcher = dispatcher.Dispatcher()
#     dispatcher.map("/debug", print)
#     dispatcher.map("/muse/eeg", eeg_handler, "EEG")
#     # dispatcher.map("/muse/elements/jaw_clench", jaw_handler, "JAW")
#     dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "Alpha")
#     dispatcher.map("/muse/elements/beta_absolute", beta_handler, "Beta")
#     dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, "Gamma")
#     dispatcher.map("/muse/elements/delta_absolute", delta_handler, "Delta")
#     dispatcher.map("/muse/elements/theta_absolute", theta_handler, "Theta")
#
#     server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#     print('\nListening at ', ip_address, ' {', port, '}')
#     server.serve_forever()