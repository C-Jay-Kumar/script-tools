module ViewMethods
    def view_class_methods(klass)
        p "methods in Class #{klass}: #{klass.instance_methods - Object.instance_methods}"
    end

    def view_class_singleton_methods(klass)
        p "methods in Singleton of Class #{klass}: #{klass.singleton_class.instance_methods - Object.instance_methods - Module.instance_methods - Class.instance_methods}"
    end

    def view_object_singleton_methods(objct)
        p "methods in Singleton of Object #{objct}: #{objct.singleton_class.instance_methods - objct.class.instance_methods}"
    end
end