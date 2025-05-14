# EchoFlow95

バージョン: `0.1.0`

Optical Flowによる運動器エコーの動態評価では、スペックルノイズにより誤差が生じやすい傾向にあります。この課題に対応するため、従来のFarneback法に基づき一定範囲の全ピクセルの動きを計算後、フレーム毎にその95パーセンタイル値を抽出・集積する手法『EchoFlow95』を考案しました。

OSはWindowsでのみ動作確認をしています。

## 使い方手順
### 1. 実行環境の構築

#### プログラムのダウンロード
こちらのページ上部に移動します。

下の画像の青丸→赤丸部分の順でクリックし、Zipファイルをダウンロードした上で、お使いのPCで解凍して下さい。

![demo1](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo1.png)

#### コマンドプロンプトの起動とフォルダの移動
コマンドプロンプトは、コマンドを使ってプログラムを操作するためのツールです。Windowsでは、次の手順でコマンドプロンプトを起動できます。

検索窓でコマンドプロンプトを検索してクリックします。(Macの場合はターミナルを使用)

![demo2](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo2.png)


コマンドプロンプトに「cd」と半角スペースを入れて、先ほど解凍したフォルダをドラッグ＆ドロップして下さい。（cdはフォルダを変更するコマンド）

![demo3](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo3.png)


#### Pythonのインストール
本プログラムは、Pythonを用いて開発されているため、あらかじめPythonのインストールが必要になります。Web上にインストール方法を説明するサイトが沢山ありますので、例えば[こちら](https://udemy.benesse.co.jp/development/python-work/python-install.html)を参考にしながらPythonをお使いのPCへインストールして下さい。


#### 仮想環境の作成
仮想環境は、プロジェクトに必要なライブラリ（必要な機能を提供するコードやツール）や依存関係を他のプロジェクトやシステム全体から隔離して管理するために使用します。

まずコマンドプロンプトに以下を入力・実行して仮想環境を作ります（ここでは「venv」という名前で仮想環境を作ります）。

```bash
python -m venv venv
```

仮想環境を実行します。

```bash
venv\Scripts\activate
```
仮想環境が立ち上がれば、以下のようになります（赤丸は仮想環境下にあることを示しています）。

![demo4](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo4.png)

Macの場合、仮想環境実行のコマンドは以下となります。
```bash
source venv/bin/activate
```

#### 必要なライブラリのインストール

`pip`というライブラリをインストールするためのツールを最新の状態にアップグレードするため、コマンドプロンプトに以下を入力して実行します。
```bash
python -m pip install --upgrade pip
```

アップグレードできたら、ライブラリをインストールします。
```bash
pip install opencv-python 
```

### 2. その他、プログラム実行のために必要なもの
EchoFlow95を実行する際には、事前に次の2つが必要です。
1. 解析したい動画ファイル
2.  解析したい動画の中における、1ピクセルあたりの距離 (mm) 

#### 解析したい動画ファイル

このプロジェクトで使用するOpenCVは、以下の動画ファイル形式に対応しています。

- `.avi` (Audio Video Interleave)
- `.mp4` (MPEG-4 Video)
- `.mov` (QuickTime Movie)
- `.mkv` (Matroska Video)
- `.flv` (Flash Video)
- `.wmv` (Windows Media Video)
- `.webm` (WebM)
- `.mpg` / `.mpeg` (MPEG)

ファイルパスが長くなったり、複雑になるとプログラムが正しく動作しない場合があるので、動画ファイルは先ほど解凍したフォルダ内に入れておくことをお勧めします。

#### 解析したい動画の中における、1ピクセルあたりの距離 (mm) 
EchoFlow95では、ピクセルの動きを実際の距離に変換して出力します。
1ピクセルあたりの距離が分からない場合には、私の作成した[こちら](https://github.com/renhorikawa/calc_dist_app)のツールが利用できます。環境構築はほぼ同じなので、手順に従ってお使いください。

### 3. プログラムの実行
EchoFlow95を起動するため、コマンドプロンプトに以下を入力して下さい。

```bash
python echoflow95.py
```

### 4. EchoFlow95の操作方法

- プログラムを実行すると、**「動画ファイルの名前を入力してください (例: video.mp4):」** と出ますのでファイル名を書いて実行します。同じフォルダ内に動画が無い場合には、動画へのパスを入力して下さい。

- 次に、**「1ピクセルあたりの距離 (mm) を入力してください:」** と出ますので、数値を入力してください。

- するとウインドウが立ち上がりますので、解析したい関心領域（ROI）をマウスで指定して下さい。起点となるROIの左上をクリックしてドラッグしていくことで四角形のエリアが展開されます。ROIが指定できたらEnterキーを押してください。

![demo5](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo5.png) 

- うまくいくと、コマンドプロンプトはこのような表示になっているはずです。フレーム間の各距離、移動距離の合計、選択したROIの大きさ、利用したPythonやライブラリのバージョンが出力されます。

![demo6](https://github.com/renhorikawa/echoflow95/blob/master/assets/demo6.png) 

### 5. プログラムを次に使う場合の注意点
コマンドプロンプトの起動、cdコマンドを使ってのフォルダ移動、仮想環境の実行（作成は不要）は毎回必要です。

## 使用上の注意
この手法はROI内が全て同一方向へ動くという仮定を元にしています。使用に際しては、解剖学・運動学的視点を踏まえ、範囲内に描出されるベクトルの方向をビジュアルで確認することが必要です。

EchoFlow95は、研究・開発段階であり、まだ臨床上での使用を想定していません。他にも、Optical Flowを用いた深層学習手法など、あらゆる可能性を含めて今後も精度検証が必要です。

## ライセンスについて
このプログラムはMITライセンスの下で公開されています。詳しくは[LICENSE](https://github.com/renhorikawa/echoflow95/blob/master/LICENSE.txt)ファイルをご覧ください。

## お問い合わせ

何か質問やご意見があれば、[renhoript@gmail.com](mailto:renhoript@gmail.com) までお気軽にお知らせください。
