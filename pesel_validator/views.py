from django.shortcuts import render
from datetime import date

def validate_pesel(request):
    if request.method == 'POST':
        pesel = request.POST.get('pesel')
        is_valid, birth_date, gender = check_pesel(pesel)
        return render(request, 'pesel_validator/result.html', {
            'is_valid': is_valid,
            'birth_date': birth_date,
            'gender': gender,
            'pesel': pesel
        })
    return render(request, 'pesel_validator/form.html')

def check_pesel(pesel):
    if len(pesel) != 11 or not pesel.isdigit():
        return False, None, None

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    check_sum = sum(int(pesel[i]) * weights[i] for i in range(10))
    check_digit = (10 - (check_sum % 10)) % 10

    if check_digit != int(pesel[10]):
        return False, None, None

    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if month > 80:
        year += 1800
        month -= 80
    elif month > 60:
        year += 2200
        month -= 60
    elif month > 40:
        year += 2100
        month -= 40
    elif month > 20:
        year += 2000
        month -= 20
    else:
        year += 1900

    try:
        birth_date = date(year, month, day)
    except ValueError:
        return False, None, None

    gender = 'Female' if int(pesel[9]) % 2 == 0 else 'Male'

    return True, birth_date, gender