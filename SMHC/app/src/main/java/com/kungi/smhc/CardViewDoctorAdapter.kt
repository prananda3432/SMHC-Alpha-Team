//package com.kungi.smhc
//
//import android.view.LayoutInflater
//import android.view.ViewGroup
//import android.widget.Toast
//import androidx.recyclerview.widget.RecyclerView
//import com.bumptech.glide.Glide
//import com.bumptech.glide.request.RequestOptions
////import com.kungi.smhc.databinding.ItemCardviewDoctorBinding
//
//class CardViewDoctorAdapter (private val listDoctor: ArrayList<Doctor>) :
//    RecyclerView.Adapter<CardViewDoctorAdapter.CardViewViewHolder>() {
//    private lateinit var binding: ItemCardviewDoctorBinding
//
//    override fun onCreateViewHolder(
//        parent: ViewGroup,
//        viewType: Int
//    ): CardViewViewHolder {
//        val binding = ItemCardviewDoctorBinding.inflate(LayoutInflater.from(parent.context), parent, false)
//        return CardViewViewHolder(binding)
//    }
//
//    override fun onBindViewHolder(holder: CardViewViewHolder, position: Int) {
//        holder.bind(listDoctor[position])
//    }
//
//    override fun getItemCount(): Int =listDoctor.size
//
//    inner class CardViewViewHolder (private val binding: ItemCardviewDoctorBinding) : RecyclerView.ViewHolder(binding) {
//        fun bind(doctor: Doctor) {
//            with(binding) {
////                Glide.with(itemView.context)
////                    .load(doctor.photo)
////                    .apply(RequestOptions().override(350,550))
////                    .into(imgItemPhoto)
////
////                tvItemName.text = doctor.name
////                tvItemAddress.text = doctor.address
////
////                chatButton.setOnClickListener { Toast.makeText(itemView.context, "Connecting ${doctor.name}", Toast.LENGTH_SHORT).show() }
//            }
//        }
//    }
//}