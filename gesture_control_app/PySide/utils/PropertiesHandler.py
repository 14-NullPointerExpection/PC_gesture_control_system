'''
    @description: 用于读取和生成properties文件
    @Date: 2022-08-17
'''

# from KeyboardMap import KeyboardMap


default_properties = {
    # 系统配置
    'mouse_sensitivity': 5,  # 鼠标灵敏度
    'scroll_speed': 5,  # 页面滚动速度
    'gesture_recognition_speed': 5,  # 手势识别速度
    # 快捷手势
    # 动作类型(按键/打开网址)
    'left_action': 'press_key',
    'right_action': 'press_key',
    'up_action': 'press_key',
    'zero_action': 'press_key',
    # 按键类型
    'left_action_key': 'none',
    'right_action_key': 'none',
    'up_action_key': 'none',
    'zero_action_key': 'none',
    # 打开网址url
    'left_action_url': 'none',
    'right_action_url': 'none',
    'up_action_url': 'none',
    'zero_action_url': 'none',
}
property_labels = {
    'mouse_sensitivity': '# 鼠标灵敏度',
    'scroll_speed': '# 页面滚动速度',
    'gesture_recognition_speed': '# 手势识别速度',
    'left_action': '# left动作类型',
    'right_action': '# right动作类型',
    'up_action': '# up动作类型',
    'zero_action': '# zero动作类型',
    'left_action_key': '# left按键类型',
    'right_action_key': '# right按键类型',
    'up_action_key': '# up按键类型',
    'zero_action_key': '# zero按键类型',
    'left_action_url': '# left网址url',
    'right_action_url': '# right网址url',
    'up_action_url': '# up网址url',
    'zero_action_url': '# zero网址url'
}


class PropertyHandler:
    def __init__(self, file_name):
        self._file_name = file_name

    def get_properties(self):
        try:
            pro_file = open(self._file_name, 'r', encoding='utf-8')
        except Exception as e:
            # 配置文件不存在，则创建配置文件
            print(e)
            properties = self.generate_properties()
            if properties is None:
                return None
        else:
            properties = {}
            for line in pro_file:
                if line.startswith('#') or line.find('=') <= 0:  # 跳过注释行
                    continue
                str = line.split('=', 1)  # 以第一个等号分割字符串
                key, value = str[0].strip(), str[1].strip()  # 去除空白字符
                properties[key] = value
            pro_file.close()
            self.verify_properties(properties)
            isok = self.generate_properties(properties)
            if isok is None:
                return None
        return properties

    def generate_properties(self, properties=default_properties):
        try:
            pro_file = open(self._file_name, 'w', encoding='utf-8')
        except Exception as e:
            print(e)
            return None
        else:
            pro_file.write('# PC手势控制系统配置文件\n\n')
            for key in properties:
                pro_file.write(property_labels[key] + '\n')
                pro_file.write(key + '=' + str(properties[key]) + '\n\n')
            pro_file.close()
            return properties

    def reset_property(self, key, value):
        properties = self.get_properties()
        properties[key] = value
        self.generate_properties(properties)
        return properties[key]

    # 检验配置文件正确性，并将错误配置重置为默认值
    def verify_properties(self, properties):
        temp_keys = []
        for key in properties:
            if key not in default_properties:
                temp_keys.append(key)
        for key in temp_keys:
            del properties[key]
        for key in default_properties:
            if key not in properties:
                properties[key] = default_properties[key]
        properties['mouse_sensitivity'] = self.check_property_intvalue('mouse_sensitivity',
                                                                       properties['mouse_sensitivity'], 1, 100)
        properties['scroll_speed'] = self.check_property_intvalue('scroll_speed', properties['scroll_speed'], 1, 100)
        properties['gesture_recognition_speed'] = self.check_property_intvalue('gesture_recognition_speed',
                                                                               properties['gesture_recognition_speed'],
                                                                               1, 100)
        properties['left_action'] = self.check_action_type(properties['left_action'])
        properties['right_action'] = self.check_action_type(properties['right_action'])
        properties['up_action'] = self.check_action_type(properties['up_action'])
        properties['zero_action'] = self.check_action_type(properties['zero_action'])
        # properties['left_action_key'] = self.check_action_key(properties['left_action_key'])
        # properties['right_action_key'] = self.check_action_key(properties['right_action_key'])
        # properties['up_action_key'] = self.check_action_key(properties['up_action_key'])
        # properties['zero_action_key'] = self.check_action_key(properties['zero_action_key'])


    def check_property_intvalue(self, key, value, min_value, max_value):
        try:
            value = int(value)
            if value < min_value or value > max_value:
                raise Exception
        except Exception as e:
            value = default_properties[key]
        return value

    def check_action_type(self, type):
        if type == 'open_url':
            return 'open_url'
        else:
            return 'press_key'
    
    def check_press_key_type(self, key):
        pass
        # if KeyboardMap.key_to_ascii.has_key(key):
        #     return key
        # else:
        #     return ''

    def save_properties(self, properties):
        return self.generate_properties(properties)
