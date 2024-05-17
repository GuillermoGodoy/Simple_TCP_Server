using System.Net.Sockets;
using System.Net;

namespace Server
{
    public class Worker : BackgroundService
    {
        private readonly ILogger<Worker> _logger;
        TcpListener server = null;
        string ip = "0.0.0.0";
        int port = 11022;
        public Worker(ILogger<Worker> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                IPAddress localAddr = IPAddress.Parse(ip);
                _logger.LogInformation($"Iniciar en: {ip}:{port}");
                server = new TcpListener(localAddr, port);
                server.Start();
                StartListener();
                server.Stop();
                await Task.Delay(1000, stoppingToken);
            }
        }
        public void StartListener()
        {
            try
            {
                while (true)
                {
                    //here have the ploblem
                    //server ip: 192.168.100.9
                    //device ip: 192.168.100.96
                    TcpClient client = server.AcceptTcpClient();
                    _logger.LogInformation($"{DateTimeOffset.Now}Device Connected!: {((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString()}");
                    Thread t = new Thread(new ParameterizedThreadStart(HandleDeivce));
                    t.Start(client);
                }
            }
            catch (SocketException e)
            {
                _logger.LogWarning("StartListener ");
                _logger.LogWarning("SocketException: " + e);
                server.Stop();
            }
        }
        public void HandleDeivce(Object obj)
        {
            TcpClient client = (TcpClient)obj;
            string ipactual = ((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString();
            _logger.LogInformation($"Device Connected!: {ipactual}");
            client.Close();
        }
    }
}
