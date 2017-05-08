QGraphicsScene *s = new QGraphicsScene();
ui->graphicsView->setScene(s);
ui->graphicsView->setRenderHint(QPainter::Antialiasing);
 
QNEBlock *b = new QNEBlock(0, s);
b->addPort("test", 0, QNEPort::NamePort);
b->addPort("TestBlock", 0, QNEPort::TypePort);
b->addInputPort("in1");
b->addInputPort("in2");
b->addInputPort("in3");
b->addOutputPort("out1");
b->addOutputPort("out2");
b->addOutputPort("out3");
 
b = b->clone();
b->setPos(150, 0);
 
b = b->clone();
b->setPos(150, 150);
 
nodesEditor = new QNodesEditor(this);
nodesEditor->install(s);
