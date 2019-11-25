web_helloc = """
两数之和(只有这个可以用)
---
tags:
  - (只有这个可以用)
parameters:
  - name: num1
    in: query
    type: string
    required: true
    description: 第一个数
  - name: num2
    in: query
    type: string
    required: true
    description: 第二个数
responses:
  500:
    description: 服务器GG
    schema:
      properties:
        name:
          type: string
          description: 名称
          default: xiaom
  200:
    description: 计算成功，返回结果
    schema:
      properties:
        name:
          type: string
          description: 名称
          default: xiaom
"""

default = """
默认标题
---
tags:
  - 测试标签
parameters:
  - name: name
    in: path
    type: string
    required: true
    description: 名称
responses:
  500:
    description: 你好像传错了
    schema:
      properties:
        name:
          type: string
          description: 名称
          default: xiaom
  200:
    description: 测试通过，下一位
    schema:
      properties:
        name:
          type: string
          description: 名称
          default: xiaom
"""
