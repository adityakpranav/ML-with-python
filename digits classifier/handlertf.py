import cv2
import tensorflow as tf
import numpy as np
class handler:
    graph=None
    img=None
    I=None
    O=None
    pkeep=None
    def __init__(self):
         self.graph=self.load_graph("static\\graph\\optimized_tfdroid.pb")
         self.I = self.graph.get_tensor_by_name('prefix/Placeholder/I:0')   
         self.O = self.graph.get_tensor_by_name('prefix/Accuracy/O:0')   
         self.pkeep=self.graph.get_tensor_by_name('prefix/Placeholder/p:0') 
	
    def convert(self,img):
        #converting image as per need
        img=img.rsplit(",")
        img.pop()
        img.append('0')
        temp=[]
        for i in range(1,78401):
            image=img[i*4-1]
            if (image=='0'):    
                temp.append(0)
            else:
                temp.append(int(image))
        img=np.asarray(temp,dtype=np.float32)

        cv=cv2.resize(np.reshape(img,(280,280)),(28,28))


        self.img=np.reshape(cv,(-1,784))
        res=str(self.predict()[0])

        return(res)







   
    def predict(self):
        with tf.Session(graph=self.graph) as sess:

            return(sess.run(self.O,{self.I:np.reshape(self.img,(-1,784)),self.pkeep:1}))


    def predicttest(self,imag):
        print("in prediction in predicttest")
        with tf.Session(graph=self.graph) as sess:
            return(sess.run(self.O,{self.I:imag,self.pkeep:1}))
	


	
    def load_graph(self,frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
        with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())

	# Then, we can use again a convenient built-in function to import a graph_def into the 
	# current default Graph
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(
				graph_def, 
				input_map=None, 
				return_elements=None, 
				name="prefix", 
				op_dict=None, 
				producer_op_list=None
			)
        return graph


