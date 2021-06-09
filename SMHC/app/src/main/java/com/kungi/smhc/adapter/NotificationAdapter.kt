package com.kungi.smhc.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.RecyclerView
import com.kungi.smhc.R
import com.kungi.smhc.data.Notification


class NotificationAdapter (private val notifList : ArrayList<Notification>) : RecyclerView.Adapter<NotificationAdapter.Holder>() {

    var context : Context? = null

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val itemView = LayoutInflater.from(parent.context).inflate(
            R.layout.list_notification, parent,false)
        this.context = parent.context
        return Holder(itemView)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {

        val currentitem = notifList[position]

        holder.title.text = currentitem.title
        holder.prioritas.text = currentitem.priority
        holder.wrapper.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View?) {
                Toast.makeText(context, "id "+getItemId(position).toString(), Toast.LENGTH_LONG)
//                moveFragment(getItemId(position))
            }
        })
    }

    private fun moveFragment(itemId: Long) {

    }

    override fun getItemCount(): Int {
        return notifList.size
    }

    override fun getItemId(position: Int): Long {
        return super.getItemId(position)
    }

    class Holder (data : View) : RecyclerView.ViewHolder (data) {
        val title : TextView = itemView.findViewById(R.id.txt_warning)
        val prioritas : TextView = itemView.findViewById(R.id.txt_lokasi)
        val wrapper : CardView = itemView.findViewById(R.id.itemWrapper)
    }
}