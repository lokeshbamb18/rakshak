class Register:
    '''
        Class for registering images based on FFT. The usage is as follows:
        >>> im0 = imread('image0.jpg', flatten = True)
        >>> im1 = imread('image1.jpg', flatten = True)
        >>> reg = Register(im0, im1)
        >>> shift = reg.shift
        >>> rotation = reg.theta

        Note:
            1. This image registration technique is not very reliable and
               is valid only for small rotation
            2. The class is very slow, since it depends on canny edge detection
               module for finding edges.
    '''
    def __init__(self,imin0, imin1, PROCESSED = False):
        '''
            This method is used to execute all the routines required to get the
            shift and the rotation
        '''
        # find edges to remove low frequency signals and suppress information
        if PROCESSED:
            im0 = imin0
            im1 = imin1
        else:
            im0 = Canny(imin0, 0.85, 5).grad
            im1 = Canny(imin1, 0.85, 5).grad

        # A major drawback of this method is that it can operate only on square
        # images. Hence we will make square image of any input image

        im0 = self.createsquareim(self.clearBorder(im0))
        im1 = self.createsquareim(self.clearBorder(im1))

        self.shift = self.findShift(im0,im1)
        imtrans = shift(im1, self.shift)
        # Remove the shift in the image. This is mandatory before we find theta
        impolar0 = self.makePolar(im0)
        impolar1 = self.makePolar(imtrans)
        self.index = self.findShift(impolar0, impolar1)[1]
        self.theta = ((self.index*90.0)/impolar1.shape[0])

    def clearBorder(self,im,width = 50, color = 255):
        '''
            A little house keeping to clear any border noise
        '''
        im[:,:width] = color
        im[:,-width:] = color
        im[:width,:] = color
        im[-width:,:] = color

        return im

    def createsquareim(self, im):
        """
        function createsquareim
        input:numpy ndarray
        output:numpy ndarray

        The function takes in an image array and converts it into square
        image by creating empty columns and rows.
        """
        lenmax = max(im.shape[0],im.shape[1])
        imout = zeros((lenmax,lenmax))
        imout[:,:] = 255
        imout[:im.shape[0],:im.shape[1]] = im
        return imout

    def findShift(self, im0, im1):
        '''
            This method is based on fft method of registering images.
        '''
        IM0 = fft2(im0)
        IM1 = fft2(im1)

        numer = IM0*conj(IM1)
        denom = abs(IM0*IM1)

        pulse_im = ifft2(numer/denom)
        mag = abs(pulse_im)
        x, y = where(mag == mag.max())

        x = array(x.tolist())   # Issues with read only arrays
        y = array(y.tolist())

        X, Y = im0.shape

        if x > X/2:
            x -= X
        if y > Y/2:
            y -= Y

        return [x[0], y[0]]

    def makePolar(self, im):
        '''
            This method will convert the cartesian coordinates image
            to polar coordinates image. The relation between the two
            domains is
              F(r,theta) = f(r*cos(theta),r*sin(theta))
            To make the process fast, we are using map_coordinates function
        '''
        m, n = im.shape
        r_max = hypot(m, n)

        r_mat = zeros_like(im)
        t_mat = zeros_like(im)

        r_mat.T[:] = linspace(0, r_max, m)
        t_mat[:] = linspace(0, pi/2, n)

        x = r_mat*cos(t_mat)
        y = r_mat*sin(t_mat)

        imout = zeros_like(im)
        imout = map_coordinates(im, [x, y], cval = 255)

        return imout
