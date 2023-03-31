from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import sklearn
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect

COLOR = {
    0: 'Blue',
    1: 'Blue-White',
    2: 'Orange',
    3: 'Orange-Red',
    4: 'Pale Yellow-Orange',
    5: 'Red',
    6: 'White',
    7: 'White-Yellow',
    8: 'Whitish',
    9: 'Yellow-White',
    10: 'Yellowish'
}

CLASS = {
    0: 'A',
    1: 'B',
    2: 'F',
    3: 'G',
    4: 'K',
    5: 'M',
    6: 'O'
}

TYPE = {
    0: 'Red Dwarf',
    1: 'Brown Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'SuperGiants',
    5: 'HyperGiants'
}


def homePageView(request):
    return render(request, 'home.html')


def predictPageView(request):
    return render(request, 'predict.html')


def reportPageView(request):
    return render(request, 'report.html')


def predictPost(request):
    try:
        temp = int(request.POST['temperature'])
        luminosity = request.POST['luminosity']
        radius = request.POST['radius']
        magnitude = request.POST['absolute-magnitude']
        colour = int(request.POST['star-colour'])
        spectral_class = int(request.POST['spectral-class'])
    except:
        return render(request, 'predict.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        return HttpResponseRedirect(reverse('results',
                                            kwargs={'temp': temp, 'luminosity': luminosity,
                                                    'radius': radius, 'magnitude': magnitude,
                                                    'colour': colour, 'spectral_class': spectral_class}))


def results(request, temp, luminosity, radius, magnitude, colour, spectral_class):
    with open('./model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('./sc_x.pkl', 'rb') as scaler_file:
        sc_x = pickle.load(scaler_file)

    sampleDf = pd.DataFrame(columns=['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)',
                                     'Absolute magnitude(Mv)', 'Star color code'])
    sampleDf = sampleDf.append({
        'Temperature (K)': temp, 'Luminosity(L/Lo)': float(luminosity),
        'Radius(R/Ro)': float(radius), 'Absolute magnitude(Mv)': float(magnitude),
        'Star color code': colour
    }, ignore_index=True)

    X_pred = sc_x.transform(sampleDf)
    prediction = model.predict(X_pred)
    colour_str = COLOR[colour]
    class_str = CLASS[spectral_class]

    return render(request, 'results.html', {'temp': temp, 'luminosity': luminosity,
                                            'radius': radius, 'magnitude': magnitude,
                                            'colour': colour_str, 'spectral_class': class_str,
                                            'type': TYPE[prediction[0]]})


def resultPageView(request):
    return render(request, 'results.html')


def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title})
