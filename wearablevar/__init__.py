import numpy as np
import pandas as pd
import datetime as datetime

'''
    Compute Wearable Variability Metrics:
    This algorithm contains 10 functions with 21 features for feature engineering of wearables data. It contains 2 functions to import and format wearables data. 
    Input:
        If using our import functions: filename (string): filename to .csv with Datetime in first column (format: format='%Y-%m-%d %H:%M:%S.%f') and the sensor data in the second column. Use E4FileFormatter.ipynb at dbdp.org for Empatica E4 files.
        If using functions only: dataframe with three columns: Time, Sensor, Day **For TOR, TIR, POR, sampling rate is required.
    Metrics computed:
        Interday Mean 
        Interday Median 
        Interday Maximum 
        Interday Minimum 
        Interday Standard Deviation 
        Interday Coefficient of Variation 
        Intraday Standard Deviation (mean, median, standard deviation)
        Intraday Coefficient of Variation (mean, median, standard deviation)
        Intraday Mean (mean, median, standard deviation)
        TIR (Time in Range of default 1 SD)
        TOR (Time outside Range of default 1 SD)
        POR (Percent outside Range of default 1 SD)
        MASE (Mean Amplitude of Sensor Excursions, default 1 SD)
        Q1G (intraday first quartile glucose)
        Q3G (intraday third quartile glucose)
        ** for more information on these variability metrics see dbdp.org**
        
    '''


def importe4(filename):
    """
        Function for importing and formatting for use with other functions.
        Args:
            filename (string): filename to a .csv with 2 columns - one with time in format = '%Y-%m-%d %H:%M:%S.%f', and the other column being the sensor value
        Returns:
            df (pandas.DataFrame): 
    """
    df = pd.read_csv(filename, header=None, names=['Time', 'Sensor']) 
    df['Time'] =  pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df['Day'] = df['Time'].dt.date
    df = df.reset_index()
    return df

def importe4acc(filename):
    """
        Function for importing and formatting for use with other functions.
        Args:
            filename (string): filename to a .csv with 4 columns - one with time in format = '%Y-%m-%d %H:%M:%S.%f', and the other columns being x,y,z of tri-axial accelerometry
        Returns:
            df (pandas.DataFrame): 
    """
    df = pd.read_csv(filename, header=None, names=['Time', 'X', 'Y', 'Z']) 
    df['Time'] =  pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df['Day'] = df['Time'].dt.date
    df['ri'] = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)
    df['Sensor'] = df['ri'] - 64
    df = df.drop(columns=['ri', 'X', 'Y', 'Z'])
    df = df.reset_index()
    return df


def interdaycv(df):
    """
        computes the interday coefficient of variation on pandas dataframe Sensor column
        Args:
            df (pandas.DataFrame):
        Returns:
            cvx (IntegerType): interday coefficient of variation 
    """
    cvx = (np.std(df['Sensor']) / (np.nanmean(df['Sensor'])))*100
    return cvx

def interdaysd(df):
    """
        computes the interday standard deviation of pandas dataframe Sensor column
        Args:
             df (pandas.DataFrame):
        Returns:
            interdaysd (IntegerType): interday standard deviation 
    """
    interdaysd = np.std(df['Sensor'])
    return interdaysd

def intradaycv(df):
    """
        computes the intradaycv, returns the mean, median, and sd of intraday cv Sensor column in pandas dataframe
        Args:
             df (pandas.DataFrame):
        Returns:
            intradaycv_mean (IntegerType): Mean, Median, and SD of intraday coefficient of variation 
            intradaycv_median (IntegerType): Median of intraday coefficient of variation 
            intradaycv_sd (IntegerType): SD of intraday coefficient of variation 
    """
    intradaycv = []
    
    for i in pd.unique(df['Day']):
        intradaycv.append(interdaycv_(df[df['Day']==i]))
    
    intradaycv_mean = np.mean(intradaycv)
    intradaycv_median = np.median(intradaycv)
    intradaycv_sd = np.std(intradaycv)
    
    return intradaycv_mean, intradaycv_median, intradaycv_sd

def intradaysd(df):
    """
        computes the intradaysd, returns the mean, median, and sd of intraday sd Sensor column in pandas dataframe
        Args:
             df (pandas.DataFrame):
        Returns:
            intradaysd_mean (IntegerType): Mean, Median, and SD of intraday standard deviation 
            intradaysd_median (IntegerType): Median of intraday standard deviation 
            intradaysd_sd (IntegerType): SD of intraday standard deviation 
    """
    intradaysd =[]
    for i in pd.unique(df['Day']):
        intradaysd.append(np.std(df[df['Day']==i]))
    
    intradaysd_mean = np.mean(intradaysd)
    intradaysd_median = np.median(intradaysd)
    intradaysd_sd = np.std(intradaysd)
    
    return intradaysd_mean, intradaysd_median, intradaysd_sd

def intradaymean(df):
    """
        computes the intradaymean, returns the mean, median, and sd of the intraday mean of the Sensor data
        Args:
             df (pandas.DataFrame):
        Returns:
            intradaysd_mean (IntegerType): Mean, Median, and SD of intraday standard deviation of glucose
            intradaysd_median (IntegerType): Median of intraday standard deviation of glucose
            intradaysd_sd (IntegerType): SD of intraday standard deviation of glucose
    """
    intradaymean =[]
    for i in pd.unique(df['Day']):
        intradaymean.append(np.mean(df[df['Day']==i]))
    
    intradaymean_mean = np.mean(intradaymean)
    intradaymean_median = np.median(intradaymean)
    intradaymean_sd = np.std(intradaymean)

    return intradaymean_mean, intradaymean_median, intradaymean_sd


def TIR(df, sd=1, sr=1):
    """
        computes time in the range of (default=1 sd from the mean) sensor column in pandas dataframe
        Args:
             df (pandas.DataFrame):
             sd (IntegerType): standard deviation from mean for range calculation (default = 1 SD)
             sr (IntegerType): 
        Returns:
            TIR (IntegerType): Time in Range set by sd, *Note time is relative to your SR
            
    """
    up = np.mean(df['Sensor']) + sd*np.std(df['Sensor'])
    dw = np.mean(df['Sensor']) - sd*np.std(df['Sensor'])
    TIR = len(df[(df['Sensor']<= up) & (df['Sensor']>= dw)])*sr 
    return TIR



def TOR(df, sd=1, sr=1):
    """
        computes time outside the range of (default=1 sd from the mean) glucose column in pandas dataframe
        Args:
             df (pandas.DataFrame):
             sd (IntegerType): standard deviation from mean for range calculation (default = 1 SD)
             sr (IntegerType): 
        Returns:
            TOR (IntegerType): Time outside of range set by sd, *Note time is relative to your SR
    """
    up = np.mean(df['Sensor']) + sd*np.std(df['Sensor'])
    dw = np.mean(df['Sensor']) - sd*np.std(df['Sensor'])
    TOR = len(df[(df['Sensor']>= up) | (df['Sensor']<= dw)])*sr
    return TOR


def POR(df, sd=1, sr=1):
    """
        computes percent time outside the range of (default=1 sd from the mean) sensor column in pandas dataframe
        Args:
             df (pandas.DataFrame):
             sd (IntegerType): standard deviation from mean for range calculation (default = 1 SD)
             sr (IntegerType): 
        Returns:
            POR (IntegerType): percent of time spent outside range set by sd
    """
    up = np.mean(df['Sensor']) + sd*np.std(df['Sensor'])
    dw = np.mean(df['Sensor']) - sd*np.std(df['Sensor'])
    TOR = len(df[(df['Sensor']>= up) | (df['Sensor']<= dw)])*sr
    POR = (TOR/(len(df)*sr))*100
    return POR


def MASE(df, sd=1):
    """
        computes the mean amplitude of sensor excursions (default = 1 sd from the mean)
        Args:
             df (pandas.DataFrame):
             sd (IntegerType): standard deviation from mean to set as a sensor excursion (default = 1 SD)
        Returns:
           MASE (IntegerType): Mean Amplitude of sensor excursions
    """
    up = np.mean(df['Sensor']) + sd*np.std(df['Sensor'])
    dw = np.mean(df['Sensor']) - sd*np.std(df['Sensor'])
    MASE = np.mean(df[(df['Sensor']>= up) | (df['Sensor']<= dw)])
    return MASE



def summarymetrics(df):
    """
        computes interday mean, median, minimum and maximum, and first and third quartile 
        Args:
             df (pandas.DataFrame):
        Returns:
            interdaymean (FloatType): mean 
            interdaymedian (FloatType): median 
            interdaymin (FloatType): minimum 
            interdaymax (FloatType): maximum 
            interdayQ1 (FloatType): first quartile 
            interdayQ3 (FloatType): third quartile 
    """
    interdaymean = np.nanmean(df['Sensor'])
    interdaymedian = np.nanmedian(df['Sensor'])
    interdaymin = np.nanmin(df['Sensor'])
    interdaymax = np.nanmax(df['Sensor'])
    interdayQ1 = np.nanpercentile(df['Sensor'], 25)
    interdayQ3 = np.nanpercentile(df['Sensor'], 75)
    
    return interdaymean, interdaymedian, interdaymin, interdaymax, interdayQ1, interdayQ3
