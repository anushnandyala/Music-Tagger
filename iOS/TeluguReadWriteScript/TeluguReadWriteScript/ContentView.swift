//
//  ContentView.swift
//  TeluguReadWriteScript
//
//  Created by Anush Nandyala on 6/1/23.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        
        ZStack {
            Color(red: 0.243, green: 0.706, blue: 0.537) // #3eb489
                .ignoresSafeArea()
            
            VStack {
                
                Image("teluguTitle")
                    .resizable()
                    .frame(width: 500, height: 250)
                    .aspectRatio(contentMode: .fit)
                    .padding([.top, .leading, .trailing], 100.0)
                    
                Text("Learn to Read and Write in Telugu").font(/*@START_MENU_TOKEN@*/.largeTitle/*@END_MENU_TOKEN@*/).fontWeight(.semibold).multilineTextAlignment(.center)
            }
            
        }
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
