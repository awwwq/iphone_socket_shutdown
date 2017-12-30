//
//  ViewController.swift
//  shut
//
//  Created by 许明旺 on 2017/12/29.
//  Copyright © 2017年 许明旺. All rights reserved.
//

import UIKit
import Starscream

class ViewController: UIViewController {
    
    let socket=WebSocket(url:URL(string: "ws://192.168.1.100:5000")!,protocols:["chat", "superchat"])
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        socket.delegate = self
    }
    
    @IBOutlet weak var label1: UILabel!
    @IBOutlet weak var button1: UIButton!
    @IBAction func buttoncon(_ sender: Any) {
        socket.connect()

    }
    
    @IBAction func buttondis(_ sender: Any) {
        socket.disconnect()
        
    }
    
    @IBOutlet weak var textfield: UITextField!
    @IBAction func sd(_ sender: Any) {
        if socket.isConnected{
            socket.write(string: "shutdown"+textfield.text!)
            label1.text = "定时关机："+textfield.text!
        }
        else{
            label1.text = "链接未建立"
        }
    }
    @IBAction func cancle(_ sender: Any) {
        if socket.isConnected{
            socket.write(string: "cancle")
            label1.text = "取消关机"
        }
        else{
            label1.text = "链接未建立"
        }
    }
}
extension ViewController:WebSocketDelegate{
    func websocketDidConnect(socket: WebSocketClient) {
        //print("websocket is connected")
        //s.write(data: Data(bytes:[0x0b],count:1))
        label1.text = "connect"
        button1.isEnabled = false
    }
    
    func websocketDidDisconnect(socket: WebSocketClient, error: Error?) {
        label1.text = "disconnect"
        button1.isEnabled = true
        //      if let e = error {
        //          print("websocket is disconnected: \(e.localizedDescription)")
        //      } else {
        //          print("websocket disconnected")
        //      }
    }
    
    func websocketDidReceiveMessage(socket: WebSocketClient, text: String) {
        //print("Received text: \(text)")
        label1.text = text
    }
    
    func websocketDidReceiveData(socket: WebSocketClient, data: Data) {
        //print("Received data: \(data.count)")
        label1.text = "2"
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

