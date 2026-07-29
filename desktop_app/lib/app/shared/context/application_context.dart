class ApplicationContext {
  /// Context-aware class holding active configuration state.
  /// Decouples business components from hardcoded variables, allowing seamless
  /// transition to authentication-driven multi-tenant sessions in the future.
  final String currentCompanyId;

  const ApplicationContext({
    this.currentCompanyId = 'dc555b36-ede8-432c-a8b9-a31294c8308a',
  });
}
