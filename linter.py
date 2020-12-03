import pylint.lint
pylint_opts = ['app.py', 'dataget.py']
pylint.lint.Run(pylint_opts)
