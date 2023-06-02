//
//  ContentView.swift
//  TeluguReadWriteScript
//
//  Created by Anush Nandyala on 6/1/23.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        
        Image("teluguTitle")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .padding(.all, 100.0)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
