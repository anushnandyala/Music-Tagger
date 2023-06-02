//
//  ContentView.swift
//  TeluguReadWriteScript
//
//  Created by Anush Nandyala on 6/1/23.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        
        VStack {
            Image("teluguTitle")
                .resizable()
                .frame(width: 500, height: 250)
                .aspectRatio(contentMode: .fit)
                .padding(.all, 100.0)
                
            Text("Learn How to Read and Write in Telugu")
        }
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
