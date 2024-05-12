def calculate_average(numbers):
  # Bug: We're adding the numbers but dividing by one less than the length
  total_sum = sum(numbers)
  average = total_sum / (len(numbers) - 1)  # This is incorrect
  return average
