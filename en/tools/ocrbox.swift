// 이미지의 글자 줄 위치(픽셀)와 내용: 한글이 들어간 줄만 지우기 위해 사용
import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let W = Double(cg.width), H = Double(cg.height)
  let req = VNRecognizeTextRequest(); req.recognitionLevel = .accurate; req.recognitionLanguages = ["ko-KR", "en-US"]; req.usesLanguageCorrection = false
  try? VNImageRequestHandler(cgImage: cg).perform([req])
  for o in req.results ?? [] {
    guard let c = o.topCandidates(1).first else { continue }
    let b = o.boundingBox
    print("\(path)\t\(Int(b.minX * W))\t\(Int((1 - b.maxY) * H))\t\(Int(b.maxX * W))\t\(Int((1 - b.minY) * H))\t\(c.string)")
  }
}
