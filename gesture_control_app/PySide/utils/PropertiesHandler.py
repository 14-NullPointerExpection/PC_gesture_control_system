'''
    @description: 用于读取和生成properties文件
    @Date: 2022-08-17
'''

default_properties = {
    'mouse_sensitivity': 5, # 鼠标灵敏度
    'scroll_speed': 5, # 页面滚动速度
    'gesture_recognition_speed': 5 # 手势识别速度
}
property_labels = {
    'mouse_sensitivity': '# 鼠标灵敏度',
    'scroll_speed': '# 页面滚动速度',
    'gesture_recognition_speed': '# 手势识别速度'
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
                if line.startswith('#') or line.find('=') <= 0: # 跳过注释行
                    continue
                str = line.split('=', 1) # 以第一个等号分割字符串
                key, value = str[0].strip(), str[1].strip() # 去除空白字符
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
            pro_file.write('# PC手势控制系统配置文件\n\n# 系统配置:\n\n')
            for key in properties:
                pro_file.write(property_labels[key] + '\n')
                pro_file.write(key + '=' + str(properties[key]) + '\n')
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
        properties['mouse_sensitivity'] = self.check_property_intvalue('mouse_sensitivity', properties['mouse_sensitivity'], 1, 100)
        properties['scroll_speed'] = self.check_property_intvalue('scroll_speed', properties['scroll_speed'], 1, 100)
        properties['gesture_recognition_speed'] = self.check_property_intvalue('gesture_recognition_speed', properties['gesture_recognition_speed'], 1, 100)

    def check_property_intvalue(self, key, value, min_value, max_value):
        try:
            value = int(value)
            if value < min_value or value > max_value:
                raise Exception
        except Exception as e:
            value = default_properties[key]
        return value

    def save_properties(self, properties):
        return self.generate_properties(properties)
