//
//  ContentView.swift
//  TeluguReadWriteScript
//
//  Created by Anush Nandyala on 6/1/23.
//

import SwiftUI

struct ContentView: View {
    
    var body: some View {
        
        NavigationStack{
            
            ZStack {
                /*Color(red: 0.243, green: 0.706, blue: 0.537) // #3eb489
                    .ignoresSafeArea()*/
                
                VStack {
                    
                    Image("teluguTitle")
                        .resizable()
                        .frame(width: 500, height: 250)
                        .aspectRatio(contentMode: .fit)
                        .padding([.top, .leading, .trailing], 100.0)
                        
                    Text("Learn to Read & Write in Telugu").font(.system(size: 50)).fontWeight(.semibold).multilineTextAlignment(.center)
                    
                    Button("Begin") {
                        print("Begin button pressed")
                    }
                    .buttonStyle(GradiantBackgroundStyle())
                    
                }
                
            }
            
        }
        
    }
}

struct GradiantBackgroundStyle: ButtonStyle {
    
    func makeBody(configuration: Self.Configuration) -> some View {
        configuration.label
            .frame(minWidth: 0, maxWidth: 200.0)
            .fontWeight(.semibold)
            .font(.largeTitle)
            .padding()
            .background(Color(red: 0.208, green: 0.22, blue: 0.224))
            .cornerRadius(40)
            .foregroundColor(.white) // #353839
            .padding(10)
            .overlay(
                    RoundedRectangle(cornerRadius: 40)
                        .stroke(Color(red: 0.208, green: 0.22, blue: 0.224), lineWidth: 8)
                )
            .frame(width: 300.0, height: 300.0/*@END_MENU_TOKEN@*/)
            .padding(.top, 150.0)
            .scaleEffect(configuration.isPressed ? 0.9 : 1.0)
            
    }
    
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
