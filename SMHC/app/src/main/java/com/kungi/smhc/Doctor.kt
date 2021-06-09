package com.kungi.smhc

import android.os.Parcelable
import kotlinx.android.parcel.Parcelize

@Parcelize
data class Doctor(
    var name: String,
    var address: String,
    var photo: String,
    var phonenumber: String
) : Parcelable
