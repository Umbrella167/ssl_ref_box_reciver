from udp import UDPMultiCastReceiver
import ssl_referee_pb2
import time
def detailed_referee_info(referee_msg):
    # 基本信息
    print("Packet Timestamp:", referee_msg.packet_timestamp)
    print("Stage:", referee_msg.stage)
    print("Command:", referee_msg.command)
    
    # 时间相关
    if referee_msg.HasField('stage_time_left'):
        print("Stage Time Left:", referee_msg.stage_time_left)
    
    # 队伍信息
    print("\nYellow Team:")
    print("  Name:", referee_msg.yellow.name)
    print("  Score:", referee_msg.yellow.score)
    print("  Red Cards:", referee_msg.yellow.red_cards)
    print("  Yellow Cards:", referee_msg.yellow.yellow_cards)
    
    print("\nBlue Team:")
    print("  Name:", referee_msg.blue.name)
    print("  Score:", referee_msg.blue.score)
    print("  Red Cards:", referee_msg.blue.red_cards)
    print("  Yellow Cards:", referee_msg.blue.yellow_cards)
    
    # 指定位置
    if referee_msg.HasField('designated_position'):
        print("\nDesignated Position:")
        print("  X:", referee_msg.designated_position.x)
        print("  Y:", referee_msg.designated_position.y)
    
    # 游戏事件
    if referee_msg.game_events:
        print("\nGame Events:")
        for event in referee_msg.game_events:
            print("  Event Type:", event.type)
def parse_referee_message(binary_data):
    referee_msg = ssl_referee_pb2.Referee()
    referee_msg.ParseFromString(binary_data)
    detailed_referee_info(referee_msg)
    # # 访问消息字段
    # print("Stage:", referee_msg.stage)
    # print("Command:", referee_msg.command)
    # print("Yellow Team Score:", referee_msg.yellow.score)
    # print("Blue Team Score:", referee_msg.blue.score)

def f(msg):
    parse_referee_message(msg[0])
a = UDPMultiCastReceiver("224.5.23.1",39991,callback=f)
while True:
    time.sleep(1)

