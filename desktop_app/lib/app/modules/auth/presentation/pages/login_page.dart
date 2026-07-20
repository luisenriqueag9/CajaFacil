import 'package:flutter/material.dart';

import '../../../../core/theme/app_radius.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../../../shared/widgets/app_button.dart';
import '../../../../shared/widgets/app_card.dart';
import '../../../../shared/widgets/app_text_field.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _usuarioController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();

  bool _ocultarContrasena = true;

  bool get _formularioCompleto {
    return _usuarioController.text.trim().isNotEmpty &&
        _contrasenaController.text.isNotEmpty;
  }

  @override
  void dispose() {
    _usuarioController.dispose();
    _contrasenaController.dispose();
    super.dispose();
  }

  void _actualizarFormulario(String _) {
    setState(() {});
  }

  void _alternarVisibilidadContrasena() {
    setState(() {
      _ocultarContrasena = !_ocultarContrasena;
    });
  }

  void _ingresar() {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        const SnackBar(
          content: Text(
            'El inicio de sesión se conectará próximamente.',
          ),
          behavior: SnackBarBehavior.floating,
          margin: EdgeInsets.all(24),
          duration: Duration(seconds: 3),
        ),
      );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Expanded(
            flex: 5,
            child: Container(
              color: Theme.of(context).colorScheme.primary,
              padding: const EdgeInsets.all(AppSpacing.xxl),
              child: const _LoginBrandSection(),
            ),
          ),
          Expanded(
            flex: 4,
            child: Container(
              color: Theme.of(context).scaffoldBackgroundColor,
              padding: const EdgeInsets.all(AppSpacing.xxl),
              child: Center(
                child: _LoginFormCard(
                  usuarioController: _usuarioController,
                  contrasenaController: _contrasenaController,
                  ocultarContrasena: _ocultarContrasena,
                  formularioCompleto: _formularioCompleto,
                  onChanged: _actualizarFormulario,
                  onTogglePassword: _alternarVisibilidadContrasena,
                  onLogin: _ingresar,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _LoginBrandSection extends StatelessWidget {
  const _LoginBrandSection();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              width: 52,
              height: 52,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(AppRadius.large),
              ),
              child: Icon(
                Icons.point_of_sale_rounded,
                color: Theme.of(context).colorScheme.primary,
                size: 30,
              ),
            ),
            const SizedBox(width: AppSpacing.md),
            const Text(
              'CajaFácil',
              style: TextStyle(
                color: Colors.white,
                fontSize: 30,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
        const Spacer(),
        const Text(
          'Administra tu negocio\ncon rapidez y claridad.',
          style: TextStyle(
            color: Colors.white,
            fontSize: 38,
            fontWeight: FontWeight.w700,
            height: 1.2,
          ),
        ),
        const SizedBox(height: AppSpacing.lg),
        const Text(
          'Ventas, inventario, clientes y reportes en un solo lugar.',
          style: TextStyle(
            color: Color(0xFFE0F7F6),
            fontSize: 17,
            height: 1.5,
          ),
        ),
        const Spacer(),
        const Text(
          'Sistema de punto de venta',
          style: TextStyle(
            color: Color(0xFFC5F0ED),
            fontSize: 13,
          ),
        ),
      ],
    );
  }
}

class _LoginFormCard extends StatelessWidget {
  const _LoginFormCard({
    required this.usuarioController,
    required this.contrasenaController,
    required this.ocultarContrasena,
    required this.formularioCompleto,
    required this.onChanged,
    required this.onTogglePassword,
    required this.onLogin,
  });

  final TextEditingController usuarioController;
  final TextEditingController contrasenaController;
  final bool ocultarContrasena;
  final bool formularioCompleto;
  final ValueChanged<String> onChanged;
  final VoidCallback onTogglePassword;
  final VoidCallback onLogin;

  @override
  Widget build(BuildContext context) {
    return AppCard(
      width: 430,
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'Bienvenido',
            style: AppTextStyles.headlineLarge,
          ),
          const SizedBox(height: AppSpacing.sm),
          const Text(
            'Ingresa tus credenciales para continuar.',
            style: AppTextStyles.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.xl),
          AppTextField(
            label: 'Usuario',
            controller: usuarioController,
            hintText: 'Escribe tu usuario',
            prefixIcon: Icons.person_outline_rounded,
            textInputAction: TextInputAction.next,
            onChanged: onChanged,
          ),
          const SizedBox(height: AppSpacing.lg),
          AppTextField(
            label: 'Contraseña',
            controller: contrasenaController,
            hintText: 'Escribe tu contraseña',
            prefixIcon: Icons.lock_outline_rounded,
            obscureText: ocultarContrasena,
            onChanged: onChanged,
            onSubmitted: formularioCompleto ? (_) => onLogin() : null,
            suffixIcon: IconButton(
              onPressed: onTogglePassword,
              tooltip: ocultarContrasena
                  ? 'Mostrar contraseña'
                  : 'Ocultar contraseña',
              icon: Icon(
                ocultarContrasena
                    ? Icons.visibility_off_outlined
                    : Icons.visibility_outlined,
              ),
            ),
          ),
          const SizedBox(height: AppSpacing.xl),
          AppButton(
            text: 'Ingresar',
            onPressed: formularioCompleto ? onLogin : null,
          ),
          const SizedBox(height: AppSpacing.lg),
          const Text(
            'Versión inicial de CajaFácil',
            textAlign: TextAlign.center,
            style: AppTextStyles.bodySmall,
          ),
        ],
      ),
    );
  }
}