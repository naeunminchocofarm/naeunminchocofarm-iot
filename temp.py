status = {
  'controllers': [
    {
      'sensors': [
        1, 2, 3
      ]
    },
    {
      'sensors': [
        4, 5
      ]
    },
    {
      'sensors': [
        6, 7, 8, 9
      ]
    }
  ]
}
data = [sensor_status for controller_status in status.get('controllers', []) for sensor_status in controller_status.get('sensors', []) ]

print(data)